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
            self.client = MongoClient(mongo_uri)
            self.db = self.client['trading_bot_db']
            
            # Definir coleções
            self.user_trades_collection = self.db['user_trades']
            self.daily_claim_collection = self.db['daily_claims']
            self.active_trades_collection = self.db['active_trades']
            self.active_users_collection = self.db['active_users']
            self.user_languages_collection = self.db['user_languages']
            self.guild_languages_collection = self.db['guild_languages']
            
            # Criar índices para otimizar consultas
            self.user_trades_collection.create_index('user_id', unique=True)
            self.daily_claim_collection.create_index('user_id', unique=True)
            self.active_trades_collection.create_index('code', unique=True)
            self.active_users_collection.create_index('user_id', unique=True)
            self.user_languages_collection.create_index('user_id', unique=True)
            self.guild_languages_collection.create_index('guild_id', unique=True)
            
            print("✅ Conexão com MongoDB estabelecida com sucesso")
            
            # Testar a conexão
            self.client.admin.command('ping')
            print("🔄 Ping ao servidor MongoDB bem-sucedido")
            
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
        return self.client is not None
    
    # ===============================================
    # Operações para Trades de Usuários
    # ===============================================
    
    def get_user_trades(self, user_id):
        """Obtém a quantidade de trades disponíveis para um usuário."""
        if not self.is_connected():
            return 0
            
        result = self.user_trades_collection.find_one({'user_id': user_id})
        return result['trades'] if result else 0
    
    def set_user_trades(self, user_id, trades_count):
        """Define a quantidade de trades para um usuário."""
        if not self.is_connected():
            return False
            
        self.user_trades_collection.update_one(
            {'user_id': user_id},
            {'$set': {'user_id': user_id, 'trades': trades_count}},
            upsert=True
        )
        return True
    
    def increment_user_trades(self, user_id, amount=1):
        """Incrementa a quantidade de trades de um usuário."""
        if not self.is_connected():
            return False
            
        self.user_trades_collection.update_one(
            {'user_id': user_id},
            {'$inc': {'trades': amount}},
            upsert=True
        )
        return True
    
    def decrement_user_trades(self, user_id, amount=1):
        """Decrementa a quantidade de trades de um usuário."""
        if not self.is_connected():
            return False
            
        self.user_trades_collection.update_one(
            {'user_id': user_id},
            {'$inc': {'trades': -amount}},
            upsert=True
        )
        return True
    
    def get_all_user_trades(self):
        """Obtém todos os registros de trades de usuários."""
        if not self.is_connected():
            return {}
            
        result = {}
        for doc in self.user_trades_collection.find():
            result[doc['user_id']] = doc['trades']
        return result
    
    # ===============================================
    # Operações para Cooldown de Claim Diário
    # ===============================================
    
    def get_last_claim_time(self, user_id):
        """Obtém o timestamp do último claim diário de um usuário."""
        if not self.is_connected():
            return None
            
        result = self.daily_claim_collection.find_one({'user_id': user_id})
        return result['timestamp'] if result else None
    
    def set_last_claim_time(self, user_id, timestamp=None):
        """Define o timestamp do último claim diário de um usuário."""
        if not self.is_connected():
            return False
            
        if timestamp is None:
            timestamp = datetime.datetime.now()
            
        self.daily_claim_collection.update_one(
            {'user_id': user_id},
            {'$set': {'user_id': user_id, 'timestamp': timestamp}},
            upsert=True
        )
        return True
    
    def get_all_claim_times(self):
        """Obtém todos os registros de timestamps de claims diários."""
        if not self.is_connected():
            return {}
            
        result = {}
        for doc in self.daily_claim_collection.find():
            result[doc['user_id']] = doc['timestamp']
        return result
    
    # ===============================================
    # Operações para Trades Ativos
    # ===============================================
    
    def get_active_trade(self, code):
        """Obtém informações de um trade ativo pelo código."""
        if not self.is_connected():
            return None
            
        result = self.active_trades_collection.find_one({'code': code})
        return result
    
    def set_active_trade(self, code, trade_info):
        """Define informações para um trade ativo."""
        if not self.is_connected():
            return False
            
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
    
    def update_active_trade_status(self, code, status):
        """Atualiza o status de um trade ativo."""
        if not self.is_connected():
            return False
            
        self.active_trades_collection.update_one(
            {'code': code},
            {'$set': {'status': status}}
        )
        return True
    
    def delete_active_trade(self, code):
        """Remove um trade ativo do banco de dados."""
        if not self.is_connected():
            return False
            
        self.active_trades_collection.delete_one({'code': code})
        return True
    
    def get_user_active_trades(self, user_id):
        """Obtém todos os trades ativos de um usuário."""
        if not self.is_connected():
            return []
            
        result = []
        for doc in self.active_trades_collection.find({'user_id': user_id}):
            result.append(doc)
        return result
    
    def get_all_active_trades(self):
        """Obtém todos os trades ativos."""
        if not self.is_connected():
            return {}
            
        result = {}
        for doc in self.active_trades_collection.find():
            code = doc.pop('code')
            result[code] = doc
        return result
    
    def delete_expired_trades(self, expire_minutes=None):
        """Remove trades expirados do banco de dados."""
        if not self.is_connected():
            return 0
            
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
    
    # ===============================================
    # Operações para Usuários com Trades Ativos
    # ===============================================
    
    def get_user_active_trade_code(self, user_id):
        """Obtém o código do trade ativo de um usuário."""
        if not self.is_connected():
            return None
            
        result = self.active_users_collection.find_one({'user_id': user_id})
        return result['active_code'] if result else None
    
    def set_user_active_trade(self, user_id, code):
        """Define o código do trade ativo para um usuário."""
        if not self.is_connected():
            return False
            
        self.active_users_collection.update_one(
            {'user_id': user_id},
            {'$set': {'user_id': user_id, 'active_code': code}},
            upsert=True
        )
        return True
    
    def remove_user_active_trade(self, user_id, code=None):
        """Remove o código do trade ativo de um usuário.
        Se code for fornecido, só remove se o código atual for igual.
        """
        if not self.is_connected():
            return False
            
        if code is not None:
            # Verificar se o usuário tem o código específico antes de remover
            result = self.active_users_collection.find_one({'user_id': user_id})
            if not result or result.get('active_code') != code:
                return False
                
        self.active_users_collection.delete_one({'user_id': user_id})
        return True
    
    def get_all_users_with_active_trades(self):
        """Obtém todos os usuários com trades ativos."""
        if not self.is_connected():
            return {}
            
        result = {}
        for doc in self.active_users_collection.find():
            result[doc['user_id']] = doc['active_code']
        return result
    
    # ===============================================
    # Operações para Preferências de Idioma
    # ===============================================
    
    def set_user_language(self, user_id, language):
        """
        Define o idioma preferido de um usuário
        
        Args:
            user_id (int): ID do usuário
            language (str): Código do idioma (pt, en, es)
        """
        if not self.is_connected():
            return False
            
        try:
            self.user_languages_collection.update_one(
                {"user_id": user_id},
                {"$set": {
                    "user_id": user_id, 
                    "language": language, 
                    "updated_at": datetime.datetime.now()
                }},
                upsert=True
            )
            return True
        except Exception as e:
            print(f"❌ Erro ao definir idioma do usuário: {e}")
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
    
    # Método de fallback para get_all_user_languages
    def get_all_user_languages(self):
        """
        Método de compatibilidade para chamadas antigas
        """
        return self.get_user_languages()
                
    def delete_user_language(self, user_id):
        """
        Remove a preferência de idioma de um usuário
        
        Args:
            user_id (int): ID do usuário
            
        Returns:
            bool: True se bem-sucedido, False caso contrário
        """
        if not self.is_connected():
            return False
            
        try:
            self.user_languages_collection.delete_one({"user_id": user_id})
            return True
        except Exception as e:
            print(f"❌ Erro ao excluir idioma do usuário: {e}")
            return False
            
    def set_guild_language(self, guild_id, language):
        """
        Define o idioma padrão de um servidor
        
        Args:
            guild_id (int): ID do servidor
            language (str): Código do idioma (pt, en, es)
            
        Returns:
            bool: True se bem-sucedido, False caso contrário
        """
        if not self.is_connected():
            return False
            
        try:
            self.guild_languages_collection.update_one(
                {"guild_id": guild_id},
                {"$set": {
                    "guild_id": guild_id, 
                    "language": language, 
                    "updated_at": datetime.datetime.now()
                }},
                upsert=True
            )
            return True
        except Exception as e:
            print(f"❌ Erro ao definir idioma do servidor: {e}")
            return False
            
    def get_guild_language(self, guild_id):
        """
        Obtém o idioma padrão de um servidor
        
        Args:
            guild_id (int): ID do servidor
            
        Returns:
            str: Código do idioma ou None se não estiver definido
        """
        if not self.is_connected():
            return None
            
        try:
            result = self.guild_languages_collection.find_one({"guild_id": guild_id})
            if result:
                return result.get("language")
            return None
        except Exception as e:
            print(f"❌ Erro ao obter idioma do servidor: {e}")
            return None
            
    def get_all_guild_languages(self):
        """
        Obtém todas as preferências de idioma dos servidores
        
        Returns:
            dict: Dicionário com IDs de servidores como chaves e códigos de idioma como valores
        """
        if not self.is_connected():
            return {}
            
        try:
            guild_languages = {}
            for doc in self.guild_languages_collection.find():
                guild_id = doc["guild_id"]
                language = doc.get("language")
                if language:
                    guild_languages[guild_id] = language
            return guild_languages
        except Exception as e:
            print(f"❌ Erro ao obter idiomas dos servidores: {e}")
            return {}
        
    def get_user_trade_history(self, user_id):
        """Retorna o histórico de trades de um usuário"""
        if not self.is_connected():
            return []
        
        try:
            collection = self.db["trade_history"]
            history = list(collection.find({"user_id": user_id}).sort("timestamp", -1))
            return history
        except Exception as e:
            print(f"Erro ao obter histórico de trades: {e}")
            return []

    def get_user_total_completed_trades(self, user_id):
        """Retorna o total de trades completados por um usuário"""
        if not self.is_connected():
            return 0
        
        try:
            collection = self.db["trade_history"]
            count = collection.count_documents({"user_id": user_id, "success": True})
            return count
        except Exception as e:
            print(f"Erro ao contar trades completados: {e}")
            return 0

    def remove_claim_cooldown(self, user_id):
        """Remove o cooldown de claim diário de um usuário"""
        if not self.is_connected():
            return False
        
        try:
            result = self.daily_claim_collection.delete_one({"user_id": user_id})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Erro ao remover cooldown: {e}")
            return False

    def get_trade_stats(self, period="all"):
        """Retorna estatísticas de trades com base no período especificado"""
        if not self.is_connected():
            return {}
        
        try:
            # Determinar data de início com base no período
            start_date = None
            now = datetime.datetime.now()
            
            if period == "today":
                start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
            elif period == "week":
                # Início da semana (segunda-feira)
                days_since_monday = now.weekday()
                start_date = (now - datetime.timedelta(days=days_since_monday)).replace(hour=0, minute=0, second=0, microsecond=0)
            elif period == "month":
                # Início do mês
                start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            
            # Definir filtro com base no período
            filter_query = {}
            if start_date:
                filter_query = {"timestamp": {"$gte": start_date}}
            
            # Coleção de histórico de trades
            collection = self.db["trade_history"]
            
            # Estatísticas básicas
            total_trades = collection.count_documents(filter_query)
            successful_trades = collection.count_documents({**filter_query, "success": True})
            failed_trades = collection.count_documents({**filter_query, "success": False})
            
            # Tempo médio de processamento
            pipeline = [
                {"$match": filter_query},
                {"$group": {
                    "_id": None,
                    "avg_time": {"$avg": "$processing_time"}
                }}
            ]
            avg_result = list(collection.aggregate(pipeline))
            avg_time = avg_result[0]["avg_time"] if avg_result else 0
            
            # Usuário mais ativo
            pipeline = [
                {"$match": filter_query},
                {"$group": {
                    "_id": "$user_id",
                    "count": {"$sum": 1}
                }},
                {"$sort": {"count": -1}},
                {"$limit": 1}
            ]
            most_active = list(collection.aggregate(pipeline))
            most_active_user_id = most_active[0]["_id"] if most_active else None
            most_active_user_count = most_active[0]["count"] if most_active else 0
            
            return {
                "total_trades": total_trades,
                "successful_trades": successful_trades,
                "failed_trades": failed_trades,
                "avg_processing_time": avg_time,
                "most_active_user_id": most_active_user_id,
                "most_active_user_count": most_active_user_count
            }
        except Exception as e:
            print(f"Erro ao obter estatísticas: {e}")
            return {}