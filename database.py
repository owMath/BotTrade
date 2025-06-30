import pymongo
from pymongo import MongoClient
import datetime
import os
from dotenv import load_dotenv

class Database:
    """Classe para gerenciar operações de banco de dados MongoDB."""
    
    def __init__(self):
        """Inicializa a conexão com o MongoDB."""
        load_dotenv()
        
        # Obter a string de conexão do MongoDB das variáveis de ambiente
        mongo_uri = os.getenv('MONGO_URI')
        if not mongo_uri:
            print("⚠️ AVISO: MONGO_URI não está configurada no arquivo .env")
            print("⚠️ O bot funcionará sem persistência de dados")
            self.client = None
            self.db = None
            return
            
        try:
            # Conectar ao MongoDB
            self.client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
            # Testar a conexão
            self.client.admin.command('ping')
            self.db = self.client['trading_bot_db']
            
            # Definir coleções
            self.user_trades_collection = self.db['user_trades']
            self.daily_claim_collection = self.db['daily_claims']
            self.active_trades_collection = self.db['active_trades']
            self.active_users_collection = self.db['active_users']
            self.user_languages_collection = self.db['user_languages']
            self.guild_languages_collection = self.db['guild_languages']
            self.slot_cooldowns_collection = self.db['slot_cooldowns'] # Coleção para cooldowns de slot
            self.box_cooldowns_collection = self.db['box_cooldowns'] # Nova coleção para cooldowns de box
            self.dice_cooldowns_collection = self.db['dice_cooldowns'] # Coleção para cooldowns de dado
            self.bets_collection = self.db['bets']
            self.bets_collection.create_index('bet_id', unique=True)
            self.giveaways_collection = self.db['giveaways']
            
            # Criar índices para otimizar consultas
            self.user_trades_collection.create_index('user_id', unique=True)
            self.daily_claim_collection.create_index('user_id', unique=True)
            self.active_trades_collection.create_index('code', unique=True)
            self.active_users_collection.create_index('user_id', unique=True)
            self.user_languages_collection.create_index('user_id', unique=True)
            self.guild_languages_collection.create_index('guild_id', unique=True)
            self.slot_cooldowns_collection.create_index('user_id', unique=True)
            self.box_cooldowns_collection.create_index('user_id', unique=True) # Novo índice para box
            self.dice_cooldowns_collection.create_index('user_id', unique=True) # Índice para dado
            
            print("✅ Conexão com MongoDB estabelecida com sucesso")
            print("🔄 Ping ao servidor MongoDB bem-sucedido")
            
        except pymongo.errors.ServerSelectionTimeoutError as e:
            print(f"❌ Timeout ao conectar ao MongoDB: {e}")
            self.client = None
            self.db = None
            print("⚠️ O bot funcionará sem persistência de dados")
        except pymongo.errors.ConnectionFailure as e:
            print(f"❌ Erro ao conectar ao MongoDB: {e}")
            self.client = None
            self.db = None
            print("⚠️ O bot funcionará sem persistência de dados")
        except Exception as e:
            print(f"❌ Erro desconhecido ao configurar MongoDB: {e}")
            self.client = None
            self.db = None
            print("⚠️ O bot funcionará sem persistência de dados")
    
    def is_connected(self):
        """Verifica se a conexão com o MongoDB está ativa."""
        if self.client is None:
            return False
            
        try:
            # Tentar fazer ping para verificar a conexão
            self.client.admin.command('ping')
            return True
        except Exception:
            return False
    
    # ===============================================
    # Operações para Trades de Usuários
    # ===============================================
    
    def get_user_trades(self, user_id):
        """Obtém a quantidade de trades disponíveis para um usuário."""
        if not self.is_connected():
            return 0
            
        try:
            result = self.user_trades_collection.find_one({'user_id': user_id})
            return result['trades'] if result else 0
        except Exception as e:
            print(f"❌ Erro ao obter trades do usuário {user_id}: {e}")
            return 0
    
    def set_user_trades(self, user_id, trades_count):
        """Define a quantidade de trades para um usuário."""
        if not self.is_connected():
            return False
            
        try:
            self.user_trades_collection.update_one(
                {'user_id': user_id},
                {'$set': {'user_id': user_id, 'trades': trades_count}},
                upsert=True
            )
            return True
        except Exception as e:
            print(f"❌ Erro ao definir trades do usuário {user_id}: {e}")
            return False
    
    def increment_user_trades(self, user_id, amount=1):
        """Incrementa a quantidade de trades de um usuário."""
        if not self.is_connected():
            return False
            
        try:
            self.user_trades_collection.update_one(
                {'user_id': user_id},
                {'$inc': {'trades': amount}},
                upsert=True
            )
            return True
        except Exception as e:
            print(f"❌ Erro ao incrementar trades do usuário {user_id}: {e}")
            return False
    
    def decrement_user_trades(self, user_id, amount=1):
        """Decrementa a quantidade de trades de um usuário."""
        if not self.is_connected():
            return False
            
        try:
            self.user_trades_collection.update_one(
                {'user_id': user_id},
                {'$inc': {'trades': -amount}},
                upsert=True
            )
            return True
        except Exception as e:
            print(f"❌ Erro ao decrementar trades do usuário {user_id}: {e}")
            return False
    
    def get_all_user_trades(self):
        """Obtém todos os registros de trades de usuários."""
        if not self.is_connected():
            return {}
            
        try:
            result = {}
            for doc in self.user_trades_collection.find():
                result[doc['user_id']] = doc['trades']
            return result
        except Exception as e:
            print(f"❌ Erro ao obter todos os trades de usuários: {e}")
            return {}
    
    # ===============================================
    # Operações para Cooldown de Claim Diário
    # ===============================================
    
    def get_last_claim_time(self, user_id):
        """Obtém o timestamp do último claim diário de um usuário."""
        if not self.is_connected():
            return None
            
        try:
            result = self.daily_claim_collection.find_one({'user_id': user_id})
            return result['timestamp'] if result else None
        except Exception as e:
            print(f"❌ Erro ao obter último claim do usuário {user_id}: {e}")
            return None
    
    def set_last_claim_time(self, user_id, timestamp=None):
        """Define o timestamp do último claim diário de um usuário."""
        if not self.is_connected():
            return False
            
        if timestamp is None:
            timestamp = datetime.datetime.now()
            
        try:
            self.daily_claim_collection.update_one(
                {'user_id': user_id},
                {'$set': {'user_id': user_id, 'timestamp': timestamp}},
                upsert=True
            )
            return True
        except Exception as e:
            print(f"❌ Erro ao definir último claim do usuário {user_id}: {e}")
            return False
    
    def get_all_claim_times(self):
        """Obtém todos os registros de timestamps de claims diários."""
        if not self.is_connected():
            return {}
            
        try:
            result = {}
            for doc in self.daily_claim_collection.find():
                result[doc['user_id']] = doc['timestamp']
            return result
        except Exception as e:
            print(f"❌ Erro ao obter todos os claims: {e}")
            return {}
    
    def remove_claim_cooldown(self, user_id):
        """Remove o cooldown de claim diário de um usuário."""
        if not self.is_connected():
            return False
            
        try:
            self.daily_claim_collection.delete_one({'user_id': user_id})
            return True
        except Exception as e:
            print(f"❌ Erro ao remover cooldown de claim do usuário {user_id}: {e}")
            return False
    
    # ===============================================
    # Operações para Cooldown de Slot
    # ===============================================
    
    def get_last_slot_time(self, user_id):
        """Obtém o timestamp do último uso do slot por um usuário."""
        if not self.is_connected():
            return None
            
        try:
            result = self.slot_cooldowns_collection.find_one({'user_id': user_id})
            return result['timestamp'] if result else None
        except Exception as e:
            print(f"❌ Erro ao obter último uso de slot do usuário {user_id}: {e}")
            return None
    
    def set_last_slot_time(self, user_id, timestamp=None):
        """Define o timestamp do último uso do slot por um usuário."""
        if not self.is_connected():
            return False
            
        if timestamp is None:
            timestamp = datetime.datetime.now()
            
        try:
            self.slot_cooldowns_collection.update_one(
                {'user_id': user_id},
                {'$set': {'user_id': user_id, 'timestamp': timestamp}},
                upsert=True
            )
            return True
        except Exception as e:
            print(f"❌ Erro ao definir último uso de slot do usuário {user_id}: {e}")
            return False
    
    def get_all_slot_times(self):
        """Obtém todos os registros de timestamps de uso do slot."""
        if not self.is_connected():
            return {}
            
        try:
            result = {}
            for doc in self.slot_cooldowns_collection.find():
                result[doc['user_id']] = doc['timestamp']
            return result
        except Exception as e:
            print(f"❌ Erro ao obter todos os cooldowns de slot: {e}")
            return {}
    
    def remove_slot_cooldown(self, user_id):
        """Remove o cooldown de slot de um usuário."""
        if not self.is_connected():
            return False
            
        try:
            self.slot_cooldowns_collection.delete_one({'user_id': user_id})
            return True
        except Exception as e:
            print(f"❌ Erro ao remover cooldown de slot do usuário {user_id}: {e}")
            return False
    
    # ===============================================
    # Operações para Cooldown de Box Game
    # ===============================================
    
    def get_last_box_time(self, user_id):
        """Obtém o timestamp do último uso do jogo da caixa por um usuário."""
        if not self.is_connected():
            return None
            
        try:
            result = self.box_cooldowns_collection.find_one({'user_id': user_id})
            return result['timestamp'] if result else None
        except Exception as e:
            print(f"❌ Erro ao obter último uso de box do usuário {user_id}: {e}")
            return None
    
    def set_last_box_time(self, user_id, timestamp=None):
        """Define o timestamp do último uso do jogo da caixa por um usuário."""
        if not self.is_connected():
            return False
            
        if timestamp is None:
            timestamp = datetime.datetime.now()
            
        try:
            self.box_cooldowns_collection.update_one(
                {'user_id': user_id},
                {'$set': {'user_id': user_id, 'timestamp': timestamp}},
                upsert=True
            )
            return True
        except Exception as e:
            print(f"❌ Erro ao definir último uso de box do usuário {user_id}: {e}")
            return False
    
    def get_all_box_times(self):
        """Obtém todos os registros de timestamps de uso do jogo da caixa."""
        if not self.is_connected():
            return {}
            
        try:
            result = {}
            for doc in self.box_cooldowns_collection.find():
                result[doc['user_id']] = doc['timestamp']
            return result
        except Exception as e:
            print(f"❌ Erro ao obter todos os cooldowns de box: {e}")
            return {}
    
    def remove_box_cooldown(self, user_id):
        """Remove o cooldown do jogo da caixa de um usuário."""
        if not self.is_connected():
            return False
            
        try:
            self.box_cooldowns_collection.delete_one({'user_id': user_id})
            return True
        except Exception as e:
            print(f"❌ Erro ao remover cooldown de box do usuário {user_id}: {e}")
            return False
    
    # ===============================================
    # Operações para Trades Ativos
    # ===============================================
    
    def get_active_trade(self, code):
        """Obtém informações de um trade ativo pelo código."""
        if not self.is_connected():
            return None
            
        try:
            result = self.active_trades_collection.find_one({'code': code})
            return result
        except Exception as e:
            print(f"❌ Erro ao obter trade ativo {code}: {e}")
            return None
    
    def set_active_trade(self, code, trade_info):
        """Define informações para um trade ativo."""
        if not self.is_connected():
            return False
            
        try:
            # Garantir que o campo 'code' existe no dicionário
            trade_info['code'] = code
            
            # Converter timestamp para datetime se for uma string
            if 'timestamp' in trade_info and isinstance(trade_info['timestamp'], str):
                try:
                    trade_info['timestamp'] = datetime.datetime.fromisoformat(trade_info['timestamp'])
                except ValueError:
                    trade_info['timestamp'] = datetime.datetime.now()
            
            self.active_trades_collection.update_one(
                {'code': code},
                {'$set': trade_info},
                upsert=True
            )
            return True
        except Exception as e:
            print(f"❌ Erro ao definir trade ativo {code}: {e}")
            return False
    
    def update_active_trade_status(self, code, status, processing_time=None):
        """Atualiza o status de um trade ativo e opcionalmente o tempo de processamento."""
        if not self.is_connected():
            return False
        try:
            update_fields = {'status': status}
            if processing_time is not None:
                update_fields['processing_time'] = processing_time
            self.active_trades_collection.update_one(
                {'code': code},
                {'$set': update_fields}
            )
            return True
        except Exception as e:
            print(f"❌ Erro ao atualizar status do trade {code}: {e}")
            return False
    
    def delete_active_trade(self, code):
        """Remove um trade ativo do banco de dados."""
        if not self.is_connected():
            return False
            
        try:
            self.active_trades_collection.delete_one({'code': code})
            return True
        except Exception as e:
            print(f"❌ Erro ao deletar trade ativo {code}: {e}")
            return False
    
    def get_user_active_trades(self, user_id):
        """Obtém todos os trades ativos de um usuário."""
        if not self.is_connected():
            return []
            
        try:
            result = []
            for doc in self.active_trades_collection.find({'user_id': user_id}):
                result.append(doc)
            return result
        except Exception as e:
            print(f"❌ Erro ao obter trades ativos do usuário {user_id}: {e}")
            return []
    
    def get_all_active_trades(self):
        """Obtém todos os trades ativos."""
        if not self.is_connected():
            return {}
            
        try:
            result = {}
            for doc in self.active_trades_collection.find():
                code = doc.pop('code')
                result[code] = doc
            return result
        except Exception as e:
            print(f"❌ Erro ao obter todos os trades ativos: {e}")
            return {}
    
    def delete_expired_trades(self, expire_minutes=None):
        """Remove trades expirados do banco de dados."""
        if not self.is_connected():
            return 0
            
        try:
            current_time = datetime.datetime.now()
            deleted_count = 0
            
            # Obter todos os trades ativos para verificar expiração
            active_trades = self.get_all_active_trades()
            for code, info in active_trades.items():
                # Se expire_minutes não for fornecido, usar o valor específico do trade
                trade_expire_minutes = expire_minutes or info.get('expire_minutes', 30)
                
                # Calcular o tempo decorrido em minutos
                if 'timestamp' in info:
                    timestamp = info['timestamp']
                    # Se timestamp for uma string, converter para datetime
                    if isinstance(timestamp, str):
                        try:
                            timestamp = datetime.datetime.fromisoformat(timestamp)
                        except ValueError:
                            continue
                    
                    elapsed_minutes = (current_time - timestamp).total_seconds() / 60
                    
                    # Se o trade expirou, removê-lo
                    if elapsed_minutes > trade_expire_minutes:
                        self.delete_active_trade(code)
                        deleted_count += 1
                        
                        # Remover o usuário da lista de usuários com trades ativos
                        user_id = info.get('user_id')
                        if user_id:
                            self.remove_user_active_trade(user_id, code)
            
            return deleted_count
        except Exception as e:
            print(f"❌ Erro ao deletar trades expirados: {e}")
            return 0
    
    # ===============================================
    # Operações para Usuários com Trades Ativos
    # ===============================================
    
    def get_user_active_trade_code(self, user_id):
        """Obtém o código do trade ativo de um usuário."""
        if not self.is_connected():
            return None
            
        try:
            result = self.active_users_collection.find_one({'user_id': user_id})
            return result['active_code'] if result else None
        except Exception as e:
            print(f"❌ Erro ao obter código de trade ativo do usuário {user_id}: {e}")
            return None
    
    def set_user_active_trade(self, user_id, code):
        """Define o código do trade ativo para um usuário."""
        if not self.is_connected():
            return False
            
        try:
            self.active_users_collection.update_one(
                {'user_id': user_id},
                {'$set': {'user_id': user_id, 'active_code': code}},
                upsert=True
            )
            return True
        except Exception as e:
            print(f"❌ Erro ao definir código de trade ativo do usuário {user_id}: {e}")
            return False
    
    def remove_user_active_trade(self, user_id, code=None):
        """Remove o código do trade ativo de um usuário.
        Se code for fornecido, só remove se o código atual for igual.
        """
        if not self.is_connected():
            return False
            
        try:
            if code is not None:
                # Verificar se o usuário tem o código específico antes de remover
                result = self.active_users_collection.find_one({'user_id': user_id})
                if not result or result.get('active_code') != code:
                    return False
                    
            self.active_users_collection.delete_one({'user_id': user_id})
            return True
        except Exception as e:
            print(f"❌ Erro ao remover trade ativo do usuário {user_id}: {e}")
            return False
    
    def get_all_users_with_active_trades(self):
        """Obtém todos os usuários com trades ativos."""
        if not self.is_connected():
            return {}
            
        try:
            result = {}
            for doc in self.active_users_collection.find():
                result[doc['user_id']] = doc['active_code']
            return result
        except Exception as e:
            print(f"❌ Erro ao obter todos os usuários com trades ativos: {e}")
            return {}
    
    # ===============================================
    # Operações para Preferências de Idioma
    # ===============================================
    
    def set_user_language(self, user_id, language):
        """
        Define o idioma preferido de um usuário no MongoDB.

        Args:
            user_id (int): ID do usuário
            language (str): Código do idioma (pt, en, es)

        Returns:
            bool: True se salvou com sucesso, False se houve erro ou não conectado
        """
        # Verifica se há conexão com o banco
        if not self.is_connected():
            print("⚠️ MongoDB não está conectado. Idioma não foi salvo.")
            return False

        try:
            # Usar operação atômica para evitar condições de corrida
            result = self.user_languages_collection.update_one(
                {"user_id": user_id},  # filtro
                {"$set": {
                    "user_id": int(user_id),  # Garantir que é um inteiro
                    "language": str(language).lower(),  # Garantir que é uma string em minúsculas
                    "updated_at": datetime.datetime.now()
                }},
                upsert=True  # Criar se não existir
            )
            
            return result.modified_count > 0 or result.upserted_id is not None
        except Exception as e:
            print(f"❌ Erro ao definir idioma do usuário {user_id}: {e}")
            return False
    
    def get_user_language(self, user_id):
        """
        Obtém o idioma preferido de um usuário
        
        Args:
            user_id (int): ID do usuário
            
        Returns:
            str: Código do idioma ou None se não estiver definido
        """
        if not self.is_connected():
            return None
            
        try:
            result = self.user_languages_collection.find_one({"user_id": user_id})
            if result:
                return result.get("language")
            return None
        except Exception as e:
            print(f"❌ Erro ao obter idioma do usuário: {e}")
            return None
    
    def get_user_languages(self):
        """
        Obtém todas as preferências de idioma dos usuários
        
        Returns:
            dict: Dicionário com IDs de usuários como chaves e códigos de idioma como valores
        """
        if not self.is_connected():
            return {}
        
        try:
            user_languages = {}
            # Corrigir consulta no MongoDB
            for doc in self.user_languages_collection.find():
                user_id = doc.get("user_id")
                language = doc.get("language")
                if user_id and language:
                    user_languages[user_id] = language
            return user_languages
        except Exception as e:
            print(f"❌ Erro ao obter idiomas dos usuários: {e}")
            return {}
    
    # ===============================================
    # Operações para Histórico de Trades
    # ===============================================
    
    def get_user_total_completed_trades(self, user_id):
        """
        Obtém o total de trades completados por um usuário
        
        Args:
            user_id (int): ID do usuário
            
        Returns:
            int: Número total de trades completados
        """
        if not self.is_connected():
            return 0
            
        # Aqui você implementaria a contagem de trades completados
        try:
            # Implementação fictícia para teste
            return 0
        except Exception as e:
            print(f"❌ Erro ao obter total de trades completados do usuário {user_id}: {e}")
            return 0
    
    # ===============================================
    # Operações para Estatísticas
    # ===============================================
    
    def get_trade_stats(self, period="all"):
        """
        Obtém estatísticas de trades para o período especificado
        
        Args:
            period (str): Período para as estatísticas (all, today, week, month)
            
        Returns:
            dict: Dicionário com estatísticas
        """
        if not self.is_connected():
            return {}
            
        try:
            # Definir o filtro de data com base no período
            now = datetime.datetime.now()
            if period == "today":
                start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
            elif period == "week":
                start_date = now - datetime.timedelta(days=7)
            elif period == "month":
                start_date = now - datetime.timedelta(days=30)
            else:  # all
                start_date = datetime.datetime.min

            # Consultar trades no período
            trades = self.active_trades_collection.find({
                "timestamp": {"$gte": start_date}
            })

            # Inicializar estatísticas
            stats = {
                'total_trades': 0,
                'successful_trades': 0,
                'failed_trades': 0,
                'total_processing_time': 0,
                'most_active_user_id': None,
                'most_active_user_count': 0
            }

            # Contador de trades por usuário
            user_trades_count = {}

            # Processar cada trade
            for trade in trades:
                stats['total_trades'] += 1
                
                # Contar trades por usuário
                user_id = trade.get('user_id')
                if user_id:
                    user_trades_count[user_id] = user_trades_count.get(user_id, 0) + 1

                # Contar sucessos e falhas
                if trade.get('status') == 'completed':
                    stats['successful_trades'] += 1
                elif trade.get('status') == 'failed':
                    stats['failed_trades'] += 1

                # Acumular tempo de processamento
                if 'processing_time' in trade:
                    stats['total_processing_time'] += trade['processing_time']

            # Calcular tempo médio de processamento
            if stats['total_trades'] > 0:
                stats['avg_processing_time'] = stats['total_processing_time'] / stats['total_trades']
            else:
                stats['avg_processing_time'] = 0

            # Encontrar usuário mais ativo
            if user_trades_count:
                most_active_user = max(user_trades_count.items(), key=lambda x: x[1])
                stats['most_active_user_id'] = most_active_user[0]
                stats['most_active_user_count'] = most_active_user[1]

            return stats
        except Exception as e:
            print(f"❌ Erro ao obter estatísticas de trades para o período {period}: {e}")
            return {}
        
    def reconnect_if_needed(self):
        """
        Tenta reconectar ao MongoDB se a conexão for perdida.
        """
        if not self.client:
            self.__init__()
            return

        try:
            self.client.admin.command('ping')
        except Exception as e:
            print(f"🔄 Reconectando ao MongoDB após falha de conexão: {e}")
            self.__init__()
            
    def bulk_update_user_trades(self, batch_data):
        """Atualiza trades de múltiplos usuários de uma vez"""
        if not self.is_connected():
            return False
        
        try:
            operations = []
            for item in batch_data:
                operations.append(pymongo.UpdateOne(
                    {'user_id': item['user_id']},
                    {'$set': item},
                    upsert=True
                ))
            
            if operations:
                self.user_trades_collection.bulk_write(operations)
            return True
        except Exception as e:
            print(f"❌ Erro ao atualizar trades em lote: {e}")
            return False
    
    def bulk_update_claim_times(self, batch_data):
        """Atualiza timestamps de claim de múltiplos usuários de uma vez"""
        if not self.is_connected():
            return False
        
        try:
            operations = []
            for item in batch_data:
                operations.append(pymongo.UpdateOne(
                    {'user_id': item['user_id']},
                    {'$set': item},
                    upsert=True
                ))
            
            if operations:
                self.daily_claim_collection.bulk_write(operations)
            return True
        except Exception as e:
            print(f"❌ Erro ao atualizar claim times em lote: {e}")
            return False
        
    def bulk_update_active_trades(self, batch_data):
        """Atualiza trades ativos de múltiplos usuários de uma vez"""
        if not self.is_connected():
            return False
        
        try:
            operations = []
            for item in batch_data:
                # Garantir que o campo 'code' existe
                if 'code' not in item:
                    continue
                
                code = item.pop('code')
                operations.append(pymongo.UpdateOne(
                    {'code': code},
                    {'$set': item},
                    upsert=True
                ))
            
            if operations:
                self.active_trades_collection.bulk_write(operations)
            return True
        except Exception as e:
            print(f"❌ Erro ao atualizar trades ativos em lote: {e}")
            return False
    
    def bulk_update_active_users(self, batch_data):
        """Atualiza usuários com trades ativos de uma vez"""
        if not self.is_connected():
            return False
        
        try:
            operations = []
            for item in batch_data:
                operations.append(pymongo.UpdateOne(
                    {'user_id': item['user_id']},
                    {'$set': item},
                    upsert=True
                ))
            
            if operations:
                self.active_users_collection.bulk_write(operations)
            return True
        except Exception as e:
            print(f"❌ Erro ao atualizar usuários ativos em lote: {e}")
            return False
    
    def bulk_update_user_languages(self, batch_data):
        """Atualiza idiomas de múltiplos usuários de uma vez"""
        if not self.is_connected():
            return False
        
        try:
            operations = []
            for item in batch_data:
                # Validações mais rigorosas
                user_id = item.get('user_id')
                language = item.get('language')
                
                if not user_id or not isinstance(user_id, int):
                    continue
                
                if language not in ['pt', 'en', 'es']:
                    continue
                
                # Garantir que o timestamp esteja presente
                updated_at = item.get('updated_at', datetime.datetime.now())
                
                operations.append(pymongo.UpdateOne(
                    {'user_id': user_id},
                    {'$set': {
                        'user_id': user_id,
                        'language': language,
                        'updated_at': updated_at
                    }},
                    upsert=True
                ))
            
            if operations:
                self.user_languages_collection.bulk_write(operations)
            return True
        except Exception as e:
            print(f"❌ Erro ao atualizar idiomas dos usuários em lote: {e}")
            return False
    
    def bulk_update_slot_times(self, batch_data):
        """Atualiza timestamps de slot de múltiplos usuários de uma vez"""
        if not self.is_connected():
            return False
        
        try:
            operations = []
            for item in batch_data:
                operations.append(pymongo.UpdateOne(
                    {'user_id': item['user_id']},
                    {'$set': item},
                    upsert=True
                ))
            
            if operations:
                self.slot_cooldowns_collection.bulk_write(operations)
            return True
        except Exception as e:
            print(f"❌ Erro ao atualizar slot times em lote: {e}")
            return False
    
    def bulk_update_box_times(self, batch_data):
        """Atualiza timestamps de box de múltiplos usuários de uma vez"""
        if not self.is_connected():
            return False
        
        try:
            operations = []
            for item in batch_data:
                operations.append(pymongo.UpdateOne(
                    {'user_id': item['user_id']},
                    {'$set': item},
                    upsert=True
                ))
            
            if operations:
                self.box_cooldowns_collection.bulk_write(operations)
            return True
        except Exception as e:
            print(f"❌ Erro ao atualizar box times em lote: {e}")
            return False
    
    # ===============================================
    # Operações para Apostas (Bets)
    # ===============================================
    def create_bet(self, bet_id, title, options, creator_id):
        """Cria uma nova aposta."""
        if not self.is_connected():
            return False
        try:
            bet_doc = {
                'bet_id': bet_id,
                'title': title,
                'options': options,  # Ex: [{'id': 1, 'text': 'Opção 1', 'votes': []}, ...]
                'creator_id': creator_id,
                'status': 'open',  # open, locked, ended
                'created_at': datetime.datetime.now(),
                'locked_at': None,
                'ended_at': None,
                'winner_option': None
            }
            self.bets_collection.insert_one(bet_doc)
            return True
        except Exception as e:
            print(f"❌ Erro ao criar aposta: {e}")
            return False

    def get_bet(self, bet_id):
        """Busca uma aposta pelo ID."""
        if not self.is_connected():
            return None
        try:
            return self.bets_collection.find_one({'bet_id': bet_id})
        except Exception as e:
            print(f"❌ Erro ao buscar aposta: {e}")
            return None

    def add_vote(self, bet_id, option_id, user_id):
        """Adiciona um voto de um usuário em uma opção."""
        if not self.is_connected():
            return False
        try:
            bet = self.get_bet(bet_id)
            if not bet or bet['status'] != 'open':
                return False
            # Remover voto anterior do usuário
            for opt in bet['options']:
                if user_id in opt['votes']:
                    opt['votes'].remove(user_id)
            # Adicionar voto na nova opção
            for opt in bet['options']:
                if opt['id'] == option_id:
                    opt['votes'].append(user_id)
            self.bets_collection.update_one({'bet_id': bet_id}, {'$set': {'options': bet['options']}})
            return True
        except Exception as e:
            print(f"❌ Erro ao adicionar voto: {e}")
            return False

    def lock_bet(self, bet_id):
        """Trava a aposta (ninguém mais pode votar)."""
        if not self.is_connected():
            return False
        try:
            self.bets_collection.update_one({'bet_id': bet_id}, {'$set': {'status': 'locked', 'locked_at': datetime.datetime.now()}})
            return True
        except Exception as e:
            print(f"❌ Erro ao travar aposta: {e}")
            return False

    def end_bet(self, bet_id, winner_option):
        """Encerra a aposta e define a opção vencedora."""
        if not self.is_connected():
            return False
        try:
            self.bets_collection.update_one({'bet_id': bet_id}, {'$set': {'status': 'ended', 'ended_at': datetime.datetime.now(), 'winner_option': winner_option}})
            return True
        except Exception as e:
            print(f"❌ Erro ao encerrar aposta: {e}")
            return False

    def delete_bet(self, bet_id):
        """Deleta uma aposta do banco de dados."""
        if not self.is_connected():
            return False
        try:
            result = self.bets_collection.delete_one({'bet_id': bet_id})
            return result.deleted_count > 0
        except Exception as e:
            print(f"❌ Erro ao deletar aposta: {e}")
            return False

    def save_giveaway(self, giveaway_id, data):
        self.giveaways_collection.update_one({'_id': giveaway_id}, {'$set': data}, upsert=True)

    def update_giveaway_participants(self, giveaway_id, participants):
        self.giveaways_collection.update_one({'_id': giveaway_id}, {'$set': {'participants': participants}})

    def get_all_active_giveaways(self):
        return list(self.giveaways_collection.find())

    def remove_giveaway(self, giveaway_id):
        self.giveaways_collection.delete_one({'_id': giveaway_id})
    
    # ===============================================
    # Operações para Cooldown de Dado
    # ===============================================
    def get_last_dice_time(self, user_id):
        """Obtém o timestamp do último uso do dado por um usuário."""
        if not self.is_connected():
            return None
        try:
            result = self.dice_cooldowns_collection.find_one({'user_id': user_id})
            return result['timestamp'] if result else None
        except Exception as e:
            print(f"❌ Erro ao obter último uso de dado do usuário {user_id}: {e}")
            return None

    def set_last_dice_time(self, user_id, timestamp=None):
        """Define o timestamp do último uso do dado por um usuário."""
        if not self.is_connected():
            return False
        if timestamp is None:
            timestamp = datetime.datetime.now()
        try:
            self.dice_cooldowns_collection.update_one(
                {'user_id': user_id},
                {'$set': {'user_id': user_id, 'timestamp': timestamp}},
                upsert=True
            )
            return True
        except Exception as e:
            print(f"❌ Erro ao definir último uso de dado do usuário {user_id}: {e}")
            return False
    
    def remove_dice_cooldown(self, user_id):
        """Remove o cooldown do dado de um usuário."""
        if not self.is_connected():
            return False
        try:
            result = self.dice_cooldowns_collection.delete_one({'user_id': user_id})
            return result.deleted_count > 0
        except Exception as e:
            print(f"❌ Erro ao remover cooldown de dado do usuário {user_id}: {e}")
            return False
    
    def reset_box_cooldown(self, user_id):
        """Reseta o cooldown do box de um usuário."""
        if not self.is_connected():
            return False
        try:
            result = self.box_cooldowns_collection.delete_one({'user_id': user_id})
            return result.deleted_count > 0
        except Exception as e:
            print(f"❌ Erro ao resetar cooldown de box do usuário {user_id}: {e}")
            return False
        