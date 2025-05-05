import discord
from discord.ext import commands
import random
import os
import datetime
import subprocess
import asyncio
from dotenv import load_dotenv
from database import Database  # Importar a classe de banco de dados
from translations import t, get_user_language as get_lang # Importar funções de tradução
from keep_alive import keep_alive

async def log_error(message, exception=None):
    print(f"[ERRO] {message}")
    if exception:
        print(f"↪️  Detalhes: {exception}")

    log_channel_id = os.getenv('LOG_CHANNEL_ID')
    if log_channel_id:
        try:
            channel = bot.get_channel(int(log_channel_id))
            if channel:
                embed = discord.Embed(
                    title="🚨 Log de Erro",
                    description=f"**{message}**",
                    color=0xff5555
                )
                if exception:
                    embed.add_field(name="Detalhes", value=f"```{str(exception)}```", inline=False)
                embed.timestamp = datetime.datetime.now()
                try:
                    await channel.send(embed=embed)
                except Exception as e:
                    print(f"❌ Falha ao enviar log para canal Discord: {e}")
        except Exception as e:
            print(f"❌ Erro ao acessar canal de log: {e}")

# Carregar variáveis de ambiente
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
TRADE_CHANNEL_ID = os.getenv('TRADE_CHANNEL_ID', '1362490549528957140')  # ID do canal específico para trades
DEFAULT_LANGUAGE = os.getenv('DEFAULT_LANGUAGE', 'pt')  # Idioma padrão do bot

# Inicializar a conexão com o banco de dados
db = Database()

# Configuração intencional para o bot
intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # Necessário para obter informações de usuários
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

# Dicionários para armazenar informações (serão sincronizados com MongoDB)
active_trades = {}
user_trades = {}
daily_claim_cooldown = {}
users_with_active_trade = {}

# Dicionário para armazenar preferências de idioma dos usuários
user_languages = {}

# Sistema de slot machine - novos dicionários
slot_cooldowns = {}
slot_reminders = {}

# Sistema de Box Game - novos dicionários
box_cooldowns = {}
box_reminders = {}

# Semáforo para limitar o número de trades simultâneos
MAX_CONCURRENT_TRADES = 2
trade_semaphore = asyncio.Semaphore(MAX_CONCURRENT_TRADES)

def generate_code(length=6):
    """Gera um código aleatório para o trade"""
    characters = 'BCDFGHKLMNPQRSTVWX23456789'
    return ''.join(random.choice(characters) for _ in range(length))

async def run_trade_process(code, expire_minutes=30, mode='trades', duration=None, trades_amount=None):
    """Executa o script main.py com os parâmetros especificados"""
    # Caminho para o script main.py
    main_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'main.py')
    
    # Variáveis de ambiente para codificação UTF-8
    env = os.environ.copy()
    env['PYTHONIOENCODING'] = 'utf-8'
    
    # Preparar argumentos para o processo
    args = ['python', main_script, code, str(expire_minutes)]
    
    # Adicionar informações de modo e duração
    if mode == 'time' and duration is not None:
        args.extend(['time', str(duration)])
    elif mode == 'trades' and trades_amount is not None:
        args.extend(['trades', str(trades_amount)])
    
    try:
        # Executar o script como um processo separado
        process = await asyncio.create_subprocess_exec(
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env=env  # Adicionando as variáveis de ambiente
        )
        
        # Esperar pela conclusão e coletar saída
        stdout, stderr = await process.communicate()
        
        # Decodificar a saída com tratamento de erros
        stdout = stdout.decode('utf-8', errors='replace')
        stderr = stderr.decode('utf-8', errors='replace')
        
        return process.returncode, stdout, stderr
    except Exception as e:
        await log_error(f"Erro ao executar processo de trade: {e}")
        return 1, "", f"Erro: {str(e)}"

# Verificador para canal de trades
def in_trade_channel():
    async def predicate(ctx):
        try:
            # Debug - imprime os IDs para verificar
            channel_id = str(ctx.channel.id)
            config_id = str(TRADE_CHANNEL_ID).strip()
            print(f"ID do canal atual: {channel_id}")
            print(f"ID do canal configurado: {config_id}")
            print(f"São iguais: {channel_id == config_id}")
            
            if not config_id:
                return True  # Se não estiver configurado, permite em qualquer canal
                
            return channel_id == config_id
        except Exception as e:
            print(f"❌ Erro ao verificar canal: {e}")
            return False
    return commands.check(predicate)

# ===============================================
# Sincronização com MongoDB e carregamento inicial de dados
# ===============================================

async def sync_data_to_mongodb():
    """Sincroniza os dicionários locais com o MongoDB periodicamente"""
    while True:
        try:
            if db.is_connected():
                # Usar lote para reduzir operações de banco de dados
                try:
                    # Lotes para operações em massa
                    user_trades_batch = []
                    daily_claim_batch = []
                    active_trades_batch = []
                    active_users_batch = []
                    user_languages_batch = []
                    slot_cooldowns_batch = []
                    box_cooldowns_batch = []
                    
                    # Preparar operações em lote para preferências de idioma
                    for user_id, lang in user_languages.items():
                        user_languages_batch.append({
                            'user_id': user_id,
                            'language': lang,
                            'updated_at': datetime.datetime.now()
                        })
                    
                    # Preparar operações em lote para cooldowns de claim diário
                    for user_id, timestamp in daily_claim_cooldown.items():
                        daily_claim_batch.append({
                            'user_id': user_id,
                            'timestamp': timestamp
                        })
                    
                    # Preparar operações em lote para trades ativos
                    for code, info in active_trades.items():
                        info_copy = info.copy()
                        info_copy['code'] = code
                        active_trades_batch.append(info_copy)
                    
                    # Preparar operações em lote para usuários com trades ativos
                    for user_id, code in users_with_active_trade.items():
                        active_users_batch.append({
                            'user_id': user_id,
                            'active_code': code
                        })
                    
                    # Preparar operações em lote para preferências de idioma
                    for user_id, lang in user_languages.items():
                        user_languages_batch.append({
                            'user_id': user_id,
                            'language': lang,
                            'updated_at': datetime.datetime.now()
                        })
                    
                    # Preparar operações em lote para cooldowns de slot
                    for user_id, timestamp in slot_cooldowns.items():
                        slot_cooldowns_batch.append({
                            'user_id': user_id,
                            'timestamp': timestamp
                        })
                    
                    # Preparar operações em lote para cooldowns de box
                    for user_id, timestamp in box_cooldowns.items():
                        box_cooldowns_batch.append({
                            'user_id': user_id,
                            'timestamp': timestamp
                        })
                    
                    # Executar sincronizações em lote, limitando o tempo para evitar bloqueios
                    await asyncio.sleep(0.1)  # Cede o controle para o loop de eventos
                    if user_trades_batch:
                        db.reconnect_if_needed()
                        db.bulk_update_user_trades(user_trades_batch)
                    
                    await asyncio.sleep(0.1)  # Cede o controle para o loop de eventos
                    if daily_claim_batch:
                        db.reconnect_if_needed()
                        db.bulk_update_claim_times(daily_claim_batch)
                    
                    await asyncio.sleep(0.1)  # Cede o controle para o loop de eventos
                    if active_trades_batch:
                        db.reconnect_if_needed()
                        db.bulk_update_active_trades(active_trades_batch)
                    
                    await asyncio.sleep(0.1)  # Cede o controle para o loop de eventos
                    if active_users_batch:
                        db.reconnect_if_needed()
                        db.bulk_update_active_users(active_users_batch)
                    
                    await asyncio.sleep(0.1)  # Cede o controle para o loop de eventos
                    if user_languages_batch:
                        try:
                            # Filtrar dados inválidos antes da sincronização
                            valid_languages_batch = [
                                item for item in user_languages_batch 
                                if item.get('user_id') and item.get('language') in ['pt', 'en', 'es']
                            ]
                            
                            if valid_languages_batch:
                                db.reconnect_if_needed()
                                db.bulk_update_user_languages(valid_languages_batch)
                        except Exception as e:
                            await log_error(f"Erro ao sincronizar linguagens de usuário em lote: {e}")
                    
                    await asyncio.sleep(0.1)  # Cede o controle para o loop de eventos
                    if slot_cooldowns_batch:
                        db.reconnect_if_needed()
                        db.bulk_update_slot_times(slot_cooldowns_batch)
                    
                    await asyncio.sleep(0.1)  # Cede o controle para o loop de eventos
                    if box_cooldowns_batch:
                        db.reconnect_if_needed()
                        db.bulk_update_box_times(box_cooldowns_batch)
                    
                    print("🔄 Dados sincronizados com MongoDB (modo lote)")
                except Exception as e:
                    await log_error("Erro durante sincronização em lote", e)
                    
                    # Fallback para o método original em caso de erro no modo lote
                    print("⚠️ Usando método de sincronização de backup")
                    
                    # Limitar o número de sincronizações por ciclo para evitar bloqueios
                    max_sync_per_category = 10
                    
                    # Sincronizar apenas um subconjunto de trades de usuários
                    for i, (user_id, trades_count) in enumerate(list(user_trades.items())[:max_sync_per_category]):
                        try:
                            db.reconnect_if_needed()
                            db.set_user_trades(user_id, trades_count)
                            await asyncio.sleep(0.01)  # Pequena pausa para o heartbeat
                        except Exception as e:
                            await log_error(f"Erro ao sincronizar trades de {user_id}", e)
                    
                    # Sincronizar apenas um subconjunto de cooldowns de claim
                    for i, (user_id, timestamp) in enumerate(list(daily_claim_cooldown.items())[:max_sync_per_category]):
                        try:
                            db.reconnect_if_needed()
                            db.set_last_claim_time(user_id, timestamp)
                            await asyncio.sleep(0.01)  # Pequena pausa para o heartbeat
                        except Exception as e:
                            await log_error(f"Erro ao sincronizar cooldown de {user_id}", e)
                    
                    # (Repete para outras categorias de dados, limitando cada uma)
                    
                    print("🔄 Dados parcialmente sincronizados com MongoDB (modo fallback)")
        except Exception as e:
            await log_error("Erro durante sincronização com MongoDB", e)
                
        # Aumentar o tempo entre sincronizações para reduzir carga
        await asyncio.sleep(600)  # Sincronizar a cada 10 minutos em vez de 5

def load_data_from_mongodb():
    """Carrega os dados do MongoDB para os dicionários locais"""
    if not db.is_connected():
        print("⚠️ MongoDB não está conectado. Usando armazenamento em memória.")
        return
        
    global user_trades, daily_claim_cooldown, active_trades, users_with_active_trade, user_languages, slot_cooldowns, box_cooldowns
    
    try:
        # Carregar trades de usuários
        user_trades_data = db.get_all_user_trades()
        if user_trades_data:
            user_trades = user_trades_data
            print(f"✅ Carregados {len(user_trades)} registros de trades de usuários do MongoDB")
            
        # Carregar cooldowns de claim diário
        daily_claim_data = db.get_all_claim_times()
        if daily_claim_data:
            daily_claim_cooldown = daily_claim_data
            print(f"✅ Carregados {len(daily_claim_cooldown)} registros de cooldown de claim do MongoDB")
            
        # Carregar trades ativos
        active_trades_data = db.get_all_active_trades()
        if active_trades_data:
            active_trades = active_trades_data
            print(f"✅ Carregados {len(active_trades)} trades ativos do MongoDB")
            
        # Carregar usuários com trades ativos
        users_with_active_trade_data = db.get_all_users_with_active_trades()
        if users_with_active_trade_data:
            users_with_active_trade = users_with_active_trade_data
            print(f"✅ Carregados {len(users_with_active_trade)} usuários com trades ativos do MongoDB")
            
        # Carregar preferências de idioma
        user_languages_data = db.get_user_languages()  # Usar o novo método
        if user_languages_data:
            user_languages = user_languages_data
            print(f"✅ Carregados {len(user_languages)} preferências de idioma do MongoDB")
                
        # Carregar cooldowns de slot
        slot_cooldowns_data = db.get_all_slot_times()  # Novo método a ser implementado
        if slot_cooldowns_data:
            slot_cooldowns = slot_cooldowns_data
            print(f"✅ Carregados {len(slot_cooldowns)} registros de cooldown de slot do MongoDB")
            
        # Carregar cooldowns de box
        box_cooldowns_data = db.get_all_box_times()
        if box_cooldowns_data:
            box_cooldowns = box_cooldowns_data
            print(f"✅ Carregados {len(box_cooldowns)} registros de cooldown de box do MongoDB")
    except Exception as e:
        print(f"❌ Erro ao carregar dados do MongoDB: {e}")

# ===============================================
# Comandos de Administrador
# ===============================================

@bot.command(name='trade')
@commands.has_permissions(administrator=True)  # Restringe apenas para administradores
async def trade_command(ctx, trades_count: int = 1, expire_minutes: int = 30):
    """Comando para iniciar trades automaticamente (modo por contagem)"""
    # Obter idioma do usuário
    lang = get_user_language(ctx.author.id)
    
    try:
        # Validar quantidade de trades
        if trades_count < 1 or trades_count > 10:
            await ctx.send(t('invalid_trades_count', lang))
            return
        
        # Validar tempo de expiração
        if expire_minutes < 1 or expire_minutes > 120:
            await ctx.send(t('invalid_expiry_time', lang))
            return
        
        # Verificar o número de trades ativos do usuário
        user_trades_active = [code for code, info in active_trades.items() if info['user_id'] == ctx.author.id]
        if len(user_trades_active) + trades_count > 3:  # Limite de 3 trades ativos por usuário
            await ctx.send(t('max_active_trades', lang, {'count': len(user_trades_active)}))
            return
        
        # Verificar se há trades simultâneos disponíveis
        if not trade_semaphore.locked() and trade_semaphore._value <= 0:
            await ctx.send(t('system_busy', lang))
            return
        
        # Criar lista para armazenar códigos e mensagens
        trade_messages = []
        
        # Enviar mensagens iniciais para todos os trades
        for _ in range(trades_count):
            code = generate_code()
            
            # Armazenar informações do código
            code_info = {
                'timestamp': datetime.datetime.now(),
                'user_id': ctx.author.id,
                'status': 'pending',
                'expire_minutes': expire_minutes,  # Campo para tempo de expiração
                'mode': 'trades'  # Modo padrão: por contagem
            }
            
            active_trades[code] = code_info
            
            # Salvar no MongoDB
            if db.is_connected():
                db.set_active_trade(code, code_info)
            
            # Enviar mensagem inicial
            initial_message = await ctx.send(t('trade_code_generated', lang, {'code': code, 'minutes': expire_minutes}))
            trade_messages.append((code, initial_message))
        
        # Processar trades em paralelo
        tasks = []
        for code, message in trade_messages:
            task = asyncio.create_task(process_trade(ctx, code, message))
            tasks.append(task)
        
        await asyncio.gather(*tasks)
    except Exception as e:
        await log_error(f"Erro no comando trade: {e}")
        await ctx.send(t('command_error', lang))
    
    return


@bot.command(name='checktrademember')
@commands.has_permissions(administrator=True)  # Restringe apenas para administradores
async def checktrademember_command(ctx, member: discord.Member = None):
    """Comando para administradores verificarem quantos trades um usuário possui"""
    # Obter idioma do usuário
    lang = get_user_language(ctx.author.id)
    
    try:
        # Se não for especificado um membro, mostra uma mensagem de erro
        if not member:
            await ctx.send(t('check_trade_no_member', lang))
            return
        
        # Verificar no MongoDB primeiro se estiver conectado
        trades_count = 0
        if db.is_connected():
            trades_count = db.get_user_trades(member.id)
            # Atualizar o dicionário local se necessário
            if member.id not in user_trades or user_trades[member.id] != trades_count:
                user_trades[member.id] = trades_count
        else:
            # Se não estiver conectado ao MongoDB, usa o dicionário local
            trades_count = user_trades.get(member.id, 0)
        
        # Criar embed com as informações
        embed = discord.Embed(
            title=t('check_trade_title', lang, {'user': member.display_name}),
            color=0x00aa00
        )
        
        embed.add_field(
            name=t('check_trade_count', lang),
            value=str(trades_count),
            inline=False
        )
        
        # Se o usuário tiver um trade ativo, mostrar o código
        active_code = None
        if member.id in users_with_active_trade:
            active_code = users_with_active_trade[member.id]
        elif db.is_connected():
            active_code = db.get_user_active_trade_code(member.id)
            if active_code:
                users_with_active_trade[member.id] = active_code
        
        if active_code:
            embed.add_field(
                name=t('check_trade_active', lang),
                value=f"Código: {active_code}",
                inline=False
            )
        else:
            embed.add_field(
                name=t('check_trade_active', lang),
                value=t('check_trade_no_active', lang),
                inline=False
            )
        
        # Adicionar informação sobre último claim
        last_claim = None
        if member.id in daily_claim_cooldown:
            last_claim = daily_claim_cooldown[member.id]
        elif db.is_connected():
            last_claim = db.get_last_claim_time(member.id)
            if last_claim:
                daily_claim_cooldown[member.id] = last_claim
        
        if last_claim:
            # Calcular tempo desde o último claim
            time_diff = datetime.datetime.now() - last_claim
            hours_left = 24 - (time_diff.total_seconds() / 3600)
            
            if hours_left > 0:
                embed.add_field(
                    name=t('check_trade_last_claim', lang),
                    value=t('check_trade_cooldown', lang, {
                        'hours': int(hours_left),
                        'minutes': int((hours_left % 1) * 60)
                    }),
                    inline=False
                )
            else:
                embed.add_field(
                    name=t('check_trade_last_claim', lang),
                    value=t('check_trade_can_claim', lang),
                    inline=False
                )
        else:
            embed.add_field(
                name=t('check_trade_last_claim', lang),
                value=t('check_trade_never_claimed', lang),
                inline=False
            )
        
        # Mostrar timestamp da última claim
        if last_claim:
            embed.set_footer(text=t('check_trade_timestamp', lang, {
                'time': last_claim.strftime("%d/%m/%Y %H:%M")
            }))
        
        await ctx.send(embed=embed)
    except Exception as e:
        await log_error(f"Erro no comando checktrademember: {e}")
        await ctx.send(t('command_error', lang))

@bot.command(name='timemode')
@commands.has_permissions(administrator=True)  # Restringe apenas para administradores
async def timemode_command(ctx, duration: int = 30, expire_minutes: int = 30):
    """Comando para iniciar trades em modo tempo (processando por X minutos)"""
    # Obter idioma do usuário
    lang = get_user_language(ctx.author.id)
    
    try:
        # Validar duração
        if duration < 1 or duration > 120:
            await ctx.send(t('invalid_duration', lang))
            return
        
        # Validar tempo de expiração
        if expire_minutes < 1 or expire_minutes > 120:
            await ctx.send(t('invalid_expiry_time', lang))
            return
        
        # Verificar o número de trades ativos do usuário
        user_trades_active = [code for code, info in active_trades.items() if info['user_id'] == ctx.author.id]
        if len(user_trades_active) >= 3:  # Limite de 3 trades ativos por usuário
            await ctx.send(t('max_active_trades', lang, {'count': len(user_trades_active)}))
            return
        
        # Verificar se há trades simultâneos disponíveis
        if not trade_semaphore.locked() and trade_semaphore._value <= 0:
            await ctx.send(t('system_busy', lang))
            return
        
        # Gerar um código para o modo tempo
        code = generate_code()
        
        # Armazenar informações do código
        code_info = {
            'timestamp': datetime.datetime.now(),
            'user_id': ctx.author.id,
            'status': 'pending',
            'expire_minutes': expire_minutes,  # Campo para tempo de expiração
            'mode': 'time',  # Modo: por tempo
            'duration': duration  # Duração do processamento
        }
        
        active_trades[code] = code_info
        
        # Salvar no MongoDB
        if db.is_connected():
            db.set_active_trade(code, code_info)
        
        # Enviar mensagem inicial
        initial_message = await ctx.send(t('trade_time_mode', lang, {'code': code, 'duration': duration, 'minutes': expire_minutes}))
        
        # Processar o trade em modo tempo
        await process_trade(ctx, code, initial_message)
    except Exception as e:
        await log_error(f"Erro no comando timemode: {e}")
        await ctx.send(t('command_error', lang))
    
    return

@bot.command(name='status')
@commands.has_permissions(administrator=True)  # Restringe apenas para administradores
async def status_command(ctx, code=None):
    """Comando para verificar o status de um código (apenas para administradores)"""
    # Obter idioma do usuário
    lang = get_user_language(ctx.author.id)
    
    try:
        if not code:
            # Procurar códigos ativos do usuário
            user_trades_active = [
                (code, info) for code, info in active_trades.items() 
                if info['user_id'] == ctx.author.id
            ]
            
            if not user_trades_active:
                await ctx.send(t('no_active_trades', lang))
                return
            
            embed = discord.Embed(
                title=t('embed_active_trades', lang),
                description=t('embed_active_trades_desc', lang, {'count': len(user_trades_active)}),
                color=0x0088ff
            )
            
            for code, info in user_trades_active:
                time_diff = datetime.datetime.now() - info['timestamp']
                # Usar o tempo de expiração específico
                expire_minutes = info.get('expire_minutes', 30)
                minutes_left = max(0, expire_minutes - int(time_diff.total_seconds() / 60))
                
                status_text = info['status']
                if status_text == 'pending':
                    status_text = t('status_pending', lang)
                elif status_text == 'processing':
                    status_text = t('status_processing', lang)
                elif status_text == 'completed':
                    status_text = t('status_completed', lang)
                elif status_text == 'failed':
                    status_text = t('status_failed', lang)
                
                mode_text = t('mode_time', lang) if info.get('mode') == 'time' else t('mode_trades', lang)
                
                embed.add_field(
                    name=f"Código: {code}",
                    value=f"Status: {status_text}\nTempo restante: {minutes_left} minutos\nModo: {mode_text}",
                    inline=False
                )
            
            await ctx.send(embed=embed)
            return
        
        # Verificar um código específico
        if code not in active_trades:
            await ctx.send(t('code_not_found', lang, {'code': code}))
            return
        
        code_info = active_trades[code]
        
        # Verificar se o usuário é o dono do código ou um administrador
        if code_info['user_id'] != ctx.author.id and not ctx.author.guild_permissions.administrator:
            await ctx.send(t('not_your_code', lang))
            return
        
        # Verificar status do código
        time_diff = datetime.datetime.now() - code_info['timestamp']
        # Usar o tempo de expiração específico
        expire_minutes = code_info.get('expire_minutes', 30)
        minutes_left = max(0, expire_minutes - int(time_diff.total_seconds() / 60))
        
        status_text = code_info['status']
        if status_text == 'pending':
            status_text = t('status_pending', lang)
        elif status_text == 'processing':
            status_text = t('status_processing', lang)
        elif status_text == 'completed':
            status_text = t('status_completed', lang)
        elif status_text == 'failed':
            status_text = t('status_failed', lang)
        
        mode_text = t('mode_time', lang) if code_info.get('mode') == 'time' else t('mode_trades', lang)
        duration = code_info.get('duration', None)
        
        embed = discord.Embed(
            title=t('embed_trade_status', lang, {'code': code}),
            color=0x0088ff
        )
        embed.add_field(name="Status", value=status_text, inline=False)
        embed.add_field(name="Tempo restante", value=f"{minutes_left} minutos", inline=False)
        embed.add_field(name="Modo", value=mode_text, inline=False)
        if duration:
            embed.add_field(name="Duração", value=f"{duration} minutos", inline=False)
        
        await ctx.send(embed=embed)
    except Exception as e:
        await log_error(f"Erro no comando status: {e}")
        await ctx.send(t('command_error', lang))


@bot.command(name='abort')
async def abort_command(ctx, code=None):
    """Comando para cancelar um código de trade ativo"""
    # Obter idioma do usuário
    lang = get_user_language(ctx.author.id)
    
    try:
        if not code:
            await ctx.send(t('abort_no_code', lang))
            return
        
        # Verificar se o código existe
        if code not in active_trades:
            await ctx.send(t('code_not_found', lang, {'code': code}))
            return
        
        code_info = active_trades[code]
        
        # Verificar se o usuário é o dono do código ou um administrador
        if code_info['user_id'] != ctx.author.id and not ctx.author.guild_permissions.administrator:
            await ctx.send(t('not_your_code', lang))
            return
        
        # Remover o código do dicionário de trades ativos
        del active_trades[code]
        
        # Se o usuário tem este código como ativo, remove do dicionário de usuários com trades ativos
        user_id = code_info.get('user_id')
        if user_id in users_with_active_trade and users_with_active_trade[user_id] == code:
            del users_with_active_trade[user_id]
            
            # Atualizar no MongoDB
            if db.is_connected():
                db.remove_user_active_trade(user_id)
                db.delete_active_trade(code)
        
        # Criar embed com a confirmação
        embed = discord.Embed(
            title=t('abort_success_title', lang),
            description=t('abort_success_desc', lang, {'code': code}),
            color=0x00ff00
        )
        
        await ctx.send(embed=embed)
    except Exception as e:
        await log_error(f"Erro no comando abort: {e}")
        await ctx.send(t('command_error', lang))
    
@bot.command(name='activecodes')
@commands.has_permissions(administrator=True)  # Restringe apenas para administradores
async def activecodes_command(ctx):
    """Comando para administradores verem todos os códigos ativos no sistema"""
    # Obter idioma do usuário
    lang = get_user_language(ctx.author.id)
    
    try:
        if not active_trades:
            await ctx.send(t('no_active_codes', lang))
            return
        
        # Criar embed para mostrar os códigos
        embed = discord.Embed(
            title=t('active_codes_title', lang),
            description=t('active_codes_desc', lang, {'count': len(active_trades)}),
            color=0x0088ff
        )
        
        # Ordenar codes por timestamp (mais recentes primeiro)
        sorted_codes = sorted(
            active_trades.items(),
            key=lambda x: x[1]['timestamp'],
            reverse=True
        )
        
        # Adicionar campos para cada código
        for code, info in sorted_codes:
            # Calcular tempo restante
            time_diff = datetime.datetime.now() - info['timestamp']
            expire_minutes = info.get('expire_minutes', 30)
            minutes_left = max(0, expire_minutes - int(time_diff.total_seconds() / 60))
            
            # Obter nome do usuário
            user_id = info['user_id']
            user = ctx.guild.get_member(user_id)
            user_name = user.display_name if user else f"ID: {user_id}"
            
            # Formatar status
            status_text = info['status']
            if status_text == 'pending':
                status_text = t('status_pending', lang)
            elif status_text == 'processing':
                status_text = t('status_processing', lang)
            elif status_text == 'completed':
                status_text = t('status_completed', lang)
            elif status_text == 'failed':
                status_text = t('status_failed', lang)
            
            # Adicionar campo para o código
            embed.add_field(
                name=f"📋 {code}",
                value=f"👤 {user_name}\n⏱️ {t('time_remaining', lang)}: {minutes_left} {t('minutes', lang)}\n📊 {t('status', lang)}: {status_text}",
                inline=True
            )
        
        await ctx.send(embed=embed)
    except Exception as e:
        await log_error(f"Erro no comando activecodes: {e}")
        await ctx.send(t('command_error', lang))
    
@bot.command(name='tradeshistory', aliases=['history'])
async def tradeshistory_command(ctx, member: discord.Member = None):
    """Comando para ver o histórico de trades de um usuário"""
    # Obter idioma do usuário
    lang = get_user_language(ctx.author.id)
    
    try:
        # Se não for especificado um membro, usa o autor do comando
        if not member:
            member = ctx.author
        
        # Verificar permissões - apenas o próprio usuário ou admins podem ver histórico
        if member.id != ctx.author.id and not ctx.author.guild_permissions.administrator:
            await ctx.send(t('history_no_permission', lang))
            return
        
        # Obter histórico do MongoDB (supondo que temos uma função para isso)
        user_history = []
        trades_total = 0
        
        if db.is_connected():
            user_history = db.get_user_trade_history(member.id)
            trades_total = db.get_user_total_completed_trades(member.id)
        
        # Verificar se existem dados de histórico
        if not user_history:
            # Verificar se o usuário já realizou trades
            if member.id in user_trades and user_trades[member.id] > 0:
                await ctx.send(t('history_no_completed_trades', lang, {'user': member.display_name}))
            else:
                await ctx.send(t('history_no_trades', lang, {'user': member.display_name}))
            return
        
        # Criar embed para mostrar o histórico
        embed = discord.Embed(
            title=t('history_title', lang, {'user': member.display_name}),
            description=t('history_desc', lang, {'total': trades_total}),
            color=0x00aa00
        )
        
        # Adicionar os últimos 5 trades (ou menos, se não houver 5)
        recent_trades = user_history[:5]  # Assume que o histórico já vem ordenado pelo mais recente
        
        for i, trade in enumerate(recent_trades):
            code = trade.get('code', 'N/A')
            timestamp = trade.get('timestamp', datetime.datetime.now())
            amount = trade.get('amount', 0)
            success = trade.get('success', True)
            
            status_text = t('trade_success', lang) if success else t('trade_failed', lang)
            time_str = timestamp.strftime("%d/%m/%Y %H:%M")
            
            embed.add_field(
                name=f"#{i+1} - {code}",
                value=f"📅 {time_str}\n🔢 {t('trades_amount', lang)}: {amount}\n📊 {t('status', lang)}: {status_text}",
                inline=True
            )
        
        # Adicionar footer com informação adicional
        embed.set_footer(text=t('history_footer', lang))
        
        await ctx.send(embed=embed)
    except Exception as e:
        await log_error(f"Erro no comando tradeshistory: {e}")
        await ctx.send(t('command_error', lang))
    
@bot.command(name='resetclaim')
@commands.has_permissions(administrator=True)  # Restringe apenas para administradores
async def resetclaim_command(ctx, member: discord.Member):
    """Comando para resetar o cooldown de claim diário de um usuário"""
    # Obter idioma do usuário
    lang = get_user_language(ctx.author.id)
    
    try:
        # Verificar se o membro foi especificado
        if not member:
            await ctx.send(t('resetclaim_no_member', lang))
            return
        
        # Remover o usuário do dicionário de cooldown
        if member.id in daily_claim_cooldown:
            del daily_claim_cooldown[member.id]
            
            # Atualizar no MongoDB
            if db.is_connected():
                db.remove_claim_cooldown(member.id)
            
            await ctx.send(t('resetclaim_success', lang, {'user': member.display_name}))
        else:
            await ctx.send(t('resetclaim_not_on_cooldown', lang, {'user': member.display_name}))
    except Exception as e:
        await log_error(f"Erro no comando resetclaim: {e}")
        await ctx.send(t('command_error', lang))
        
@bot.command(name='stats')
@commands.has_permissions(administrator=True)  # Restringe apenas para administradores
async def stats_command(ctx, period: str = "all"):
    """Comando para ver estatísticas de trades no sistema"""
    # Obter idioma do usuário
    lang = get_user_language(ctx.author.id)
    
    try:
        # Verificar o período solicitado
        valid_periods = ["all", "today", "week", "month"]
        if period.lower() not in valid_periods:
            await ctx.send(t('stats_invalid_period', lang, {'periods': ", ".join(valid_periods)}))
            return
        
        # Obter estatísticas do MongoDB (assumindo funções para isso)
        stats = {}
        
        if db.is_connected():
            stats = db.get_trade_stats(period.lower())
        else:
            await ctx.send(t('stats_db_required', lang))
            return
        
        # Extrair estatísticas
        total_trades = stats.get('total_trades', 0)
        successful_trades = stats.get('successful_trades', 0)
        failed_trades = stats.get('failed_trades', 0)
        avg_time = stats.get('avg_processing_time', 0)
        most_active_user_id = stats.get('most_active_user_id', None)
        most_active_user_count = stats.get('most_active_user_count', 0)
        
        # Calcular taxa de sucesso
        success_rate = 0
        if total_trades > 0:
            success_rate = (successful_trades / total_trades) * 100
        
        # Obter nome do usuário mais ativo
        most_active_user_name = "Ninguém"
        if most_active_user_id:
            user = ctx.guild.get_member(most_active_user_id)
            if user:
                most_active_user_name = user.display_name
        
        # Formatar título com base no período
        period_title = ""
        if period.lower() == "today":
            period_title = t('stats_today', lang)
        elif period.lower() == "week":
            period_title = t('stats_week', lang)
        elif period.lower() == "month":
            period_title = t('stats_month', lang)
        else:
            period_title = t('stats_all_time', lang)
        
        # Criar embed para mostrar as estatísticas
        embed = discord.Embed(
            title=t('stats_title', lang, {'period': period_title}),
            description=t('stats_desc', lang),
            color=0x5555ff
        )
        
        # Adicionar campos de estatísticas
        embed.add_field(
            name=t('stats_total', lang),
            value=str(total_trades),
            inline=True
        )
        
        embed.add_field(
            name=t('stats_success', lang),
            value=f"{successful_trades} ({success_rate:.1f}%)",
            inline=True
        )
        
        embed.add_field(
            name=t('stats_failed', lang),
            value=str(failed_trades),
            inline=True
        )
        
        embed.add_field(
            name=t('stats_avg_time', lang),
            value=f"{avg_time:.1f} {t('seconds', lang)}",
            inline=True
        )
        
        embed.add_field(
            name=t('stats_most_active', lang),
            value=f"{most_active_user_name} ({most_active_user_count} trades)",
            inline=True
        )
        
        # Adicionar timestamp
        embed.timestamp = datetime.datetime.now()
        
        await ctx.send(embed=embed)
    except Exception as e:
        await log_error(f"Erro no comando stats: {e}")
        await ctx.send(t('command_error', lang))
    
# ===============================================
# Novos Comandos para Gerenciamento de Trades
# ===============================================

@bot.command(name='givetrade')
@commands.has_permissions(administrator=True)  # Restringe apenas para administradores
async def givetrade_command(ctx, member: discord.Member, amount: int = 1):
    """Comando para administradores darem trades a um usuário"""
    # Obter idioma do usuário
    lang = get_user_language(ctx.author.id)
    
    try:
        # Caso o membro esteja offline ou com privacidade bloqueada
        if not member:
            await ctx.send(t('member_not_found', lang))
            return
        
        if amount < 1 or amount > 100:
            await ctx.send(t('trade_amount_invalid', lang))
            return
        
        # Inicializa o dicionário do usuário se não existir
        if member.id not in user_trades:
            user_trades[member.id] = 0
        
        # Adiciona os trades ao usuário
        user_trades[member.id] += amount
        
        # Atualizar no MongoDB
        if db.is_connected():
            db.increment_user_trades(member.id, amount)
        
        # Mensagem pública no canal
        await ctx.send(t('trades_added', lang, {'amount': amount, 'user': member.display_name, 'total': user_trades[member.id]}))
        
        # Obter o objeto do canal de trades
        trade_channel = None
        if TRADE_CHANNEL_ID:
            trade_channel = bot.get_channel(int(TRADE_CHANNEL_ID))
        # Enviar mensagem privada para o usuário que recebeu os trades
        try:
            # Criar embed para a mensagem privada
            embed = discord.Embed(
                title=t('trades_received_title', lang),
                description=t('trades_received_desc', lang, {
                    'amount': amount, 
                    'admin': ctx.author.display_name,
                    'channel': trade_channel.mention if trade_channel else "#trades"
                }),
                color=0x00ff00  # Verde
                )
            
            # Campos adicionais no embed
            embed.add_field(
                name=t('current_trades', lang), 
                value=str(user_trades[member.id]), 
                inline=False
            )
            
            # Enviar mensagem via DM
            await member.send(embed=embed)
            
        except discord.Forbidden:
            # Se o usuário tiver DMs desativadas, notificar o admin
            await ctx.send(t('dm_blocked', lang, {'user': member.mention}))
        except Exception as e:
            # Lidar com outros possíveis erros de envio de DM
            print(f"❌ Erro ao enviar DM para {member.id}: {e}")
            await ctx.send(t('dm_error', lang, {'user': member.mention}))
    except Exception as e:
        await log_error(f"Erro no comando givetrade: {e}")
        await ctx.send(t('command_error', lang))

@bot.command(name='listtrades')
@in_trade_channel()  # Verifica se o comando está sendo usado no canal correto
async def listtrades_command(ctx):
    """Comando para usuários verificarem quantos trades possuem"""
    try:
        user_id = ctx.author.id
        # Obter idioma do usuário
        lang = get_user_language(user_id)
        
        # Verificar no MongoDB primeiro se estiver conectado
        if db.is_connected():
            mongo_trades = db.get_user_trades(user_id)
            # Atualizar o dicionário local se necessário
            if user_id not in user_trades or user_trades[user_id] != mongo_trades:
                user_trades[user_id] = mongo_trades
        
        if user_id not in user_trades or user_trades[user_id] <= 0:
            await ctx.send(t('no_trades_available', lang))
            return
        
        await ctx.send(t('trades_available', lang, {'count': user_trades[user_id]}))
    except Exception as e:
        user_id = ctx.author.id
        lang = get_user_language(user_id)
        await log_error(f"Erro no comando listtrades: {e}")
        await ctx.send(t('command_error', lang))

@bot.command(name='claimtrade')
@in_trade_channel()  # Verifica se o comando está sendo usado no canal correto
async def claimtrade_command(ctx):
    """Comando para usuários obterem trades diários (5 trades a cada 24 horas)"""
    try:
        user_id = ctx.author.id
        # Obter idioma do usuário
        lang = get_user_language(user_id)
        
        current_time = datetime.datetime.now()
        
        # Verificar no MongoDB primeiro se estiver conectado
        if db.is_connected():
            last_claim_time = db.get_last_claim_time(user_id)
            if last_claim_time:
                daily_claim_cooldown[user_id] = last_claim_time
        
        # Verifica o cooldown
        if user_id in daily_claim_cooldown:
            last_claim = daily_claim_cooldown[user_id]
            time_diff = current_time - last_claim
            
            # Verifica se já passaram 24 horas desde o último claim
            if time_diff.total_seconds() < 86400:  # 24 horas em segundos
                hours_left = 24 - (time_diff.total_seconds() / 3600)
                await ctx.send(t('cooldown_active', lang, {
                    'hours': int(hours_left),
                    'minutes': int((hours_left % 1) * 60)
                }))
                return
        
        # Inicializa o dicionário do usuário se não existir
        if user_id not in user_trades:
            user_trades[user_id] = 0
        
        # Adiciona 5 trades e atualiza o timestamp do último claim
        user_trades[user_id] += 5
        daily_claim_cooldown[user_id] = current_time
        
        # Atualizar no MongoDB
        if db.is_connected():
            db.increment_user_trades(user_id, 5)
            db.set_last_claim_time(user_id, current_time)
        
        await ctx.send(t('trades_claimed', lang, {'total': user_trades[user_id]}))
    except Exception as e:
        user_id = ctx.author.id
        lang = get_user_language(user_id)
        await log_error(f"Erro no comando claimtrade: {e}")
        await ctx.send(t('command_error', lang))

@bot.command(name='usetrade')
@in_trade_channel()  # Verifica se o comando está sendo usado no canal correto
async def usetrade_command(ctx, trades_amount: int = 2):
    """Comando para usuários usarem um trade disponível com quantidade específica de trades"""
    try:
        user_id = ctx.author.id
        # Obter idioma do usuário
        lang = get_user_language(user_id)
        
        # Verificar no MongoDB primeiro se estiver conectado
        if db.is_connected():
            # Verificar trades disponíveis
            mongo_trades = db.get_user_trades(user_id)
            if user_id not in user_trades or user_trades[user_id] != mongo_trades:
                user_trades[user_id] = mongo_trades
                
            # Verificar se o usuário já tem um trade ativo
            active_code = db.get_user_active_trade_code(user_id)
            if active_code:
                users_with_active_trade[user_id] = active_code
        
        # Verificar se o usuário já tem um trade em andamento
        if user_id in users_with_active_trade:
            active_code = users_with_active_trade[user_id]
            try:
                # Send this message as a DM
                await ctx.author.send(t('trade_already_active', lang, {'code': active_code}))
                # Add a reaction to indicate a DM was sent
                await ctx.message.add_reaction('✉️')
            except discord.Forbidden:
                # Usuário tem DMs bloqueadas, enviar mensagem no canal
                await ctx.send(t('trade_already_active_public', lang, {'mention': ctx.author.mention}))
                await ctx.send(t('dm_blocked', lang, {'user': ctx.author.mention}))
            return
        
        # Validar quantidade de trades
        if trades_amount < 1 or trades_amount > 10:
            await ctx.send(t('invalid_trades_count', lang))
            return
        
        # Verifica se o usuário tem trades suficientes para a quantidade solicitada
        if user_id not in user_trades or user_trades[user_id] <= 0:
            await ctx.send(t('no_trades_available', lang))
            return
        
        # Verifica se o usuário tem trades suficientes para a quantidade solicitada
        if user_trades[user_id] < trades_amount:
            await ctx.send(t('not_enough_trades', lang, {'available': user_trades[user_id], 'requested': trades_amount}))
            return
        
        # Verificar se há trades simultâneos disponíveis
        if not trade_semaphore.locked() and trade_semaphore._value <= 0:
            await ctx.send(t('system_busy', lang))
            return
        
        # Verificar se o usuário aceita DMs antes de gerar o código
        try:
            test_dm = await ctx.author.send(t('checking_dms', lang))
            await test_dm.delete()  # Deletar a mensagem de teste após verificar
        except discord.Forbidden:
            # Se o usuário tiver DMs desativadas, notificar no canal
            await ctx.send(t('dm_required', lang, {'user': ctx.author.mention}))
            return
        except Exception as e:
            # Outro erro ao enviar DM
            await log_error(f"Erro ao verificar DMs para {ctx.author.id}: {e}")
            await ctx.send(t('dm_error', lang, {'user': ctx.author.mention}))
            return
        
        # Gerar um código para o trade
        code = generate_code()
        
        # Registrar que o usuário tem um trade ativo
        users_with_active_trade[user_id] = code
        
        # Atualizar no MongoDB
        if db.is_connected():
            db.set_user_active_trade(user_id, code)
        
        # Define um tempo de expiração padrão (60 minutos)
        expire_minutes = 60
        
        # Armazenar informações do código
        code_info = {
            'timestamp': datetime.datetime.now(),
            'user_id': user_id,
            'status': 'pending',
            'expire_minutes': expire_minutes,
            'mode': 'trades',  # Modo padrão: por contagem
            'trades_amount': trades_amount  # Nova propriedade para armazenar a quantidade de trades
        }
        
        active_trades[code] = code_info
        
        # Atualizar no MongoDB
        if db.is_connected():
            db.set_active_trade(code, code_info)
        
        # Send a public message without the code
        await ctx.send(t('generating_trades', lang, {'amount': trades_amount, 'mention': ctx.author.mention}))
        
        try:
            # Send the sensitive code information via DM
            dm_message = await ctx.author.send(t('trade_processing', lang, {'amount': trades_amount, 'code': code}))
            
            # Add a reaction to indicate that a DM was sent
            await ctx.message.add_reaction('✉️')
            
            # Processar o trade com a quantidade especificada (via DM)
            await process_trade_with_dm(ctx, code, dm_message, trades_amount)
            
            # Deduzir a quantidade de trades solicitada do usuário
            user_trades[user_id] -= trades_amount
            
            # Atualizar no MongoDB
            if db.is_connected():
                db.decrement_user_trades(user_id, trades_amount)
            
            # Informar quantos trades restantes o usuário tem via DM
            await ctx.author.send(t('trades_used', lang, {'count': user_trades[user_id]}))
        except discord.Forbidden:
            # Se o usuário tiver DMs desativadas após o início do processo
            await ctx.send(t('dm_blocked_during_trade', lang, {'user': ctx.author.mention}))
            
            # Cancelar o trade e limpar dicionários
            if user_id in users_with_active_trade:
                del users_with_active_trade[user_id]
            
            if code in active_trades:
                del active_trades[code]
                
            # Atualizar no MongoDB
            if db.is_connected():
                db.remove_user_active_trade(user_id)
                db.delete_active_trade(code)
        except Exception as e:
            await log_error(f"Erro ao processar trade: {e}")
            await ctx.send(t('trade_error_public', lang, {'mention': ctx.author.mention}))
            
            # Limpar dicionários em caso de erro
            if user_id in users_with_active_trade:
                del users_with_active_trade[user_id]
            
            # Atualizar no MongoDB
            if db.is_connected():
                db.remove_user_active_trade(user_id)
        finally:
            # Remover usuário do dicionário de usuários com trades ativos
            if user_id in users_with_active_trade:
                del users_with_active_trade[user_id]
                
                # Atualizar no MongoDB
                if db.is_connected():
                    db.remove_user_active_trade(user_id)
    except Exception as e:
        user_id = ctx.author.id
        lang = get_user_language(user_id)
        await log_error(f"Erro no comando usetrade: {e}")
        await ctx.send(t('command_error', lang))
        
        # Garantir que o usuário não fique com trade preso em caso de erro
        if user_id in users_with_active_trade:
            del users_with_active_trade[user_id]
            
            # Atualizar no MongoDB
            if db.is_connected():
                db.remove_user_active_trade(user_id)

# ===============================================
# Comandos de Idioma
# ===============================================

@bot.command(name='lang', aliases=['language', 'idioma', 'idiomas'])
async def language_command(ctx, language_code=None):
    """Comando para definir ou verificar o idioma preferido"""
    try:
        user_id = ctx.author.id
        
        # Se não foi especificado um código de idioma, mostrar o atual
        if not language_code:
            current_lang = get_user_language(user_id)
            lang_names = {
                'pt': 'Português',
                'en': 'English',
                'es': 'Español',
                'de': 'Deutsch',
                'fr': 'Français',
                'it': 'Italiano',
                'pl': 'Polski'
            }
            lang_name = lang_names.get(current_lang, current_lang)
            
            # Obter o idioma para mostrar a mensagem
            await ctx.send(t('current_language', current_lang, {'language': lang_name}))
            
            # Mostrar idiomas disponíveis
            available_langs = ', '.join([f"{code} ({lang_names[code]})" for code in lang_names.keys()])
            await ctx.send(t('available_languages', current_lang, {'languages': available_langs}))
            return
        
        # Verificar se o código de idioma é válido
        language_code = language_code.lower()
        if language_code not in ['pt', 'en', 'es', 'de', 'fr', 'it', 'pl']:
            # Obter o idioma atual para a mensagem de erro
            current_lang = get_user_language(user_id)
            await ctx.send(t('invalid_language', current_lang, {'code': language_code}))
            return
        
        # Atualizar o idioma do usuário
        user_languages[user_id] = language_code
        
        # Atualizar no MongoDB
        if db.is_connected():
            db.set_user_language(user_id, language_code)
        
        # Confirmar a alteração no novo idioma
        lang_names = {
            'pt': 'Português',
            'en': 'English',
            'es': 'Español',
            'de': 'Deutsch',
            'fr': 'Français',
            'it': 'Italiano',
            'pl': 'Polski'
        }
        await ctx.send(t('language_updated', language_code, {'language': lang_names[language_code]}))
    except Exception as e:
        user_id = ctx.author.id
        current_lang = get_user_language(user_id)
        await log_error(f"Erro no comando language: {e}")
        await ctx.send(t('command_error', current_lang))

def get_user_language(user_id):
    """Obtém o idioma preferido de um usuário"""
    try:
        # Verificar no MongoDB primeiro se estiver conectado
        if db.is_connected():
            mongo_lang = db.get_user_language(user_id)
            if mongo_lang:
                user_languages[user_id] = mongo_lang
        
        # Retornar o idioma do usuário ou o padrão
        return user_languages.get(user_id, DEFAULT_LANGUAGE)
    except Exception as e:
        print(f"❌ Erro ao obter idioma do usuário {user_id}: {e}")
        return DEFAULT_LANGUAGE

# ===============================================
# Sistema de Slot Machine
# ===============================================

# Classe para o botão de lembrete
class SlotReminderButton(discord.ui.Button):
    def __init__(self, user_id, lang, slot_time):
        super().__init__(
            style=discord.ButtonStyle.primary,
            label=t('slot_reminder_button', lang),
            emoji="⏰"
        )
        self.user_id = user_id
        self.lang = lang
        self.slot_time = slot_time
        
    async def callback(self, interaction):
        try:
            # Verificar se quem clicou é o dono do botão
            if interaction.user.id != self.user_id:
                try:
                    if not interaction.response.is_done():
                        await interaction.response.send_message(
                            t('not_your_button', self.lang),
                            ephemeral=True
                        )
                    else:
                        await interaction.followup.send(
                            t('not_your_button', self.lang),
                            ephemeral=True
                        )
                except discord.NotFound:
                    # Interação expirada ou inválida
                    pass
                except Exception as e:
                    await log_error(f"Erro ao responder interação (not_your_button): {e}")
                return
                    
            # Calcular quando o lembrete deve ser enviado
            current_time = datetime.datetime.now()
            time_diff = (self.slot_time - current_time).total_seconds()
            
            if time_diff <= 0:
                # O cooldown já acabou
                try:
                    if not interaction.response.is_done():
                        await interaction.response.send_message(
                            t('slot_already_available', self.lang),
                            ephemeral=True
                        )
                    else:
                        await interaction.followup.send(
                            t('slot_already_available', self.lang),
                            ephemeral=True
                        )
                except discord.NotFound:
                    # Interação expirada ou inválida
                    pass
                except Exception as e:
                    await log_error(f"Erro ao responder interação (already_available): {e}")
                return
                    
            # Registrar o lembrete
            slot_reminders[self.user_id] = self.slot_time
            
            # Confirmar com o usuário
            try:
                if not interaction.response.is_done():
                    await interaction.response.send_message(
                        t('slot_reminder_set', self.lang, {
                            'minutes': int(time_diff / 60)
                        }),
                        ephemeral=True
                    )
                else:
                    await interaction.followup.send(
                        t('slot_reminder_set', self.lang, {
                            'minutes': int(time_diff / 60)
                        }),
                        ephemeral=True
                    )
            except discord.NotFound:
                # Interação expirada ou inválida
                pass
            except Exception as e:
                await log_error(f"Erro ao responder interação (reminder_set): {e}")
                return
            
            try:
                # Desativar o botão após o clique
                self.disabled = True
                await interaction.message.edit(view=self.view)
            except Exception as e:
                await log_error(f"Erro ao editar mensagem após clique no botão: {e}")
            
            # Agendar o lembrete
            bot.loop.create_task(send_slot_reminder(interaction.user, self.slot_time, self.lang))
        except Exception as e:
            await log_error(f"Erro no callback do botão de slot: {e}")
            try:
                if not interaction.response.is_done():
                    await interaction.response.send_message(
                        t('error_occurred', self.lang),
                        ephemeral=True
                    )
                else:
                    await interaction.followup.send(
                        t('error_occurred', self.lang),
                        ephemeral=True
                    )
            except discord.NotFound:
                # Interação expirada ou inválida
                pass
            except Exception as e:
                await log_error(f"Erro ao enviar mensagem de erro: {e}")


# View para o botão de lembrete do box
class BoxReminderView(discord.ui.View):
    def __init__(self, user_id, lang):
        super().__init__(timeout=300)  # 5 minutos de timeout
        
        try:
            # Calcular quando o box estará disponível novamente
            current_time = datetime.datetime.now()
            box_time = box_cooldowns.get(user_id, current_time)
            remind_time = box_time + datetime.timedelta(minutes=5)
            
            # Adicionar o botão de lembrete
            self.add_item(BoxReminderButton(user_id, lang, remind_time))
        except Exception as e:
            print(f"❌ Erro ao criar view de lembrete de box: {e}")

# View para o botão de lembrete
class SlotReminderView(discord.ui.View):
    def __init__(self, user_id, lang):
        super().__init__(timeout=300)  # 5 minutos de timeout
        
        try:
            # Calcular quando o slot estará disponível novamente
            current_time = datetime.datetime.now()
            slot_time = slot_cooldowns.get(user_id, current_time)
            remind_time = slot_time + datetime.timedelta(minutes=5)
            
            # Adicionar o botão de lembrete
            self.add_item(SlotReminderButton(user_id, lang, remind_time))
        except Exception as e:
            print(f"❌ Erro ao criar view de lembrete de slot: {e}")

async def send_slot_reminder(user, slot_time, lang):
    """Função para enviar o lembrete quando o cooldown do slot acabar"""
    try:
        current_time = datetime.datetime.now()
        time_diff = (slot_time - current_time).total_seconds()
        
        if time_diff > 0:
            # Esperar até o tempo do lembrete
            await asyncio.sleep(time_diff)
        
        # Verificar se o usuário ainda tem o lembrete ativado
        if user.id in slot_reminders and slot_reminders[user.id] == slot_time:
            try:
                # Enviar mensagem de lembrete via DM
                await user.send(t('slot_reminder_message', lang))
                
                # Limpar o lembrete
                del slot_reminders[user.id]
            except Exception as e:
                print(f"❌ Erro ao enviar lembrete de slot para {user.id}: {e}")
    except Exception as e:
        await log_error(f"Erro ao processar lembrete de slot: {e}")

@bot.command(name='slot')
@in_trade_channel()  # Verifica se o comando está sendo usado no canal correto
async def slot_command(ctx):
    """Comando para jogar na slot machine e ganhar trades"""
    try:
        user_id = ctx.author.id
        # Obter idioma do usuário
        lang = get_user_language(user_id)
        
        # Verificar cooldown
        current_time = datetime.datetime.now()
        if user_id in slot_cooldowns:
            last_use = slot_cooldowns[user_id]
            time_diff = current_time - last_use
            
            # Verificar se já passaram 5 minutos desde o último uso
            if time_diff.total_seconds() < 300:  # 5 minutos em segundos
                minutes_left = 5 - (time_diff.total_seconds() / 60)
                
                # Criar embed para aviso de cooldown
                embed = discord.Embed(
                    title=t('slot_cooldown_title', lang),
                    description=t('slot_cooldown_desc', lang, {
                        'minutes': int(minutes_left),
                        'seconds': int((minutes_left % 1) * 60)
                    }),
                    color=0xff9900
                )
                
                # Criar view com o botão de lembrete
                view = SlotReminderView(user_id, lang)
                
                await ctx.send(embed=embed, view=view)
                return
        
        # Emojis para o slot
        emojis = ["🍒", "🍋", "🍉", "🍇", "💰", "⭐"]
        
        # Escolhe 3 símbolos aleatórios
        results = [random.choice(emojis) for _ in range(3)]
        
        # Verificar resultado
        trades_won = 0
        result_text = ""
        
        # Todos os símbolos iguais (jackpot) = 3 trades
        if results[0] == results[1] == results[2]:
            trades_won = 3
            result_text = t('slot_jackpot', lang)
        # Dois símbolos iguais = 2 trades
        elif results[0] == results[1] or results[1] == results[2] or results[0] == results[2]:
            trades_won = 2
            result_text = t('slot_two_match', lang)
        # Nenhum símbolo igual = sem prêmio
        else:
            result_text = t('slot_no_match', lang)
        
        # Criar embed com o resultado
        embed = discord.Embed(
            title=t('slot_result_title', lang),
            description=t('slot_result_desc', lang, {'user': ctx.author.mention}),
            color=0xffcc00 if trades_won > 0 else 0xff5555
        )
        
        # Adicionar o resultado visual
        embed.add_field(
            name=t('slot_machine', lang),
            value=f"[ {results[0]} | {results[1]} | {results[2]} ]",
            inline=False
        )
        
        # Adicionar o resultado textual
        embed.add_field(
            name=t('slot_result', lang),
            value=result_text,
            inline=False
        )
        
        # Adicionar quantidade de trades ganhos
        if trades_won > 0:
            # Inicializar o usuário no dicionário se não existir
            if user_id not in user_trades:
                user_trades[user_id] = 0
                
            # Adicionar trades ganhos
            user_trades[user_id] += trades_won
            
            # Atualizar no MongoDB
            if db.is_connected():
                db.increment_user_trades(user_id, trades_won)
                
            embed.add_field(
                name=t('slot_prize', lang),
                value=t('slot_trades_won', lang, {'count': trades_won}),
                inline=False
            )
            
            embed.add_field(
                name=t('slot_total_trades', lang),
                value=t('slot_total_count', lang, {'count': user_trades[user_id]}),
                inline=False
            )
        
        # Atualizar cooldown
        slot_cooldowns[user_id] = current_time
        
        # Atualizar no MongoDB
        if db.is_connected():
            db.set_last_slot_time(user_id, current_time)
        
        # Calcular quando o próximo slot estará disponível
        next_slot_time = current_time + datetime.timedelta(minutes=5)
        
        # Criar view com o botão de lembrete para o próximo slot
        view = SlotReminderView(user_id, lang)
        
        # Enviar mensagem com o resultado e botão de lembrete
        await ctx.send(embed=embed, view=view)
    except Exception as e:
        user_id = ctx.author.id
        lang = get_user_language(user_id)
        await log_error(f"Erro no comando slot: {e}")
        await ctx.send(t('command_error', lang))

@bot.command(name='resetslot')
@commands.has_permissions(administrator=True)  # Restringe apenas para administradores
async def resetslot_command(ctx, member: discord.Member):
    """Comando para administradores resetarem o cooldown do slot de um usuário"""
    # Obter idioma do usuário
    lang = get_user_language(ctx.author.id)
    
    try:
        # Verificar se o membro foi especificado
        if not member:
            await ctx.send(t('resetslot_no_member', lang))
            return
        
        # Remover o usuário do dicionário de cooldown
        if member.id in slot_cooldowns:
            del slot_cooldowns[member.id]
            
            # Remover qualquer lembrete pendente
            if member.id in slot_reminders:
                del slot_reminders[member.id]
            
            # Atualizar no MongoDB
            if db.is_connected():
                db.remove_slot_cooldown(member.id)
            
            await ctx.send(t('resetslot_success', lang, {'user': member.display_name}))
        else:
            await ctx.send(t('resetslot_not_on_cooldown', lang, {'user': member.display_name}))
    except Exception as e:
        await log_error(f"Erro no comando resetslot: {e}")
        await ctx.send(t('command_error', lang))


# ===============================================
# Sistema de Box Game (Adivinhe a Caixa)
# ===============================================

# Classe para os botões do jogo da caixa
class BoxGameButton(discord.ui.Button):
    def __init__(self, box_number, is_winner, user_id, lang):
        # Emoji de caixa para todos os botões inicialmente
        super().__init__(style=discord.ButtonStyle.secondary, emoji="📦", custom_id=f"box_{box_number}")
        self.box_number = box_number
        self.is_winner = is_winner
        self.user_id = user_id
        self.lang = lang
        
    async def callback(self, interaction):
        try:
            # Verificar se quem clicou é o dono do jogo
            if interaction.user.id != self.user_id:
                try:
                    if not interaction.response.is_done():
                        await interaction.response.send_message(
                            t('not_your_game', self.lang),
                            ephemeral=True
                        )
                    else:
                        await interaction.followup.send(
                            t('not_your_game', self.lang),
                            ephemeral=True
                        )
                except discord.NotFound:
                    # Interação expirada ou inválida
                    pass
                except Exception as e:
                    await log_error(f"Erro ao responder interação (not_your_game): {e}")
                return
                
            # Desabilitar todos os botões para evitar múltiplas escolhas
            for item in self.view.children:
                item.disabled = True
                
                # Atualizar o emoji com base no resultado
                if isinstance(item, BoxGameButton):
                    if item.is_winner:
                        item.emoji = "🎁"  # Emoji de presente para a caixa vencedora
                        item.style = discord.ButtonStyle.success
                    else:
                        item.emoji = "❌"  # Emoji X para caixas vazias
                        item.style = discord.ButtonStyle.danger
                        
            # Verifica se o usuário ganhou
            if self.is_winner:
                # Adicionar um trade ao usuário
                if self.user_id not in user_trades:
                    user_trades[self.user_id] = 0
                    
                user_trades[self.user_id] += 1
                
                # Atualizar no MongoDB
                if db.is_connected():
                    db.increment_user_trades(self.user_id, 1)
                    
                # Criar embed com resultado vitorioso
                embed = discord.Embed(
                    title=t('box_win_title', self.lang),
                    description=t('box_win_desc', self.lang, {'box': self.box_number}),
                    color=0x00ff00
                )
                
                embed.add_field(
                    name=t('box_prize', self.lang),
                    value=t('box_trade_won', self.lang),
                    inline=False
                )
                
                embed.add_field(
                    name=t('box_total_trades', self.lang),
                    value=t('box_total_count', self.lang, {'count': user_trades[self.user_id]}),
                    inline=False
                )
                
                # Atualizar a mensagem com o resultado (sem botão de lembrete)
                try:
                    if not interaction.response.is_done():
                        await interaction.response.edit_message(embed=embed, view=self.view)
                    else:
                        await interaction.message.edit(embed=embed, view=self.view)
                except discord.NotFound:
                    # Interação expirada ou inválida
                    pass
                except Exception as e:
                    await log_error(f"Erro ao editar mensagem (vitória): {e}")
            else:
                # Criar embed com resultado de derrota
                embed = discord.Embed(
                    title=t('box_lose_title', self.lang),
                    description=t('box_lose_desc', self.lang, {'box': self.box_number}),
                    color=0xff0000
                )
                
                embed.add_field(
                    name=t('box_try_again', self.lang),
                    value=t('box_cooldown_info', self.lang),
                    inline=False
                )
                
                # Atualizar cooldown no dicionário
                current_time = datetime.datetime.now()
                box_cooldowns[self.user_id] = current_time
                
                # Atualizar no MongoDB
                if db.is_connected():
                    db.set_last_box_time(self.user_id, current_time)
                
                # Criar nova view que inclui o botão de lembrete
                result_view = discord.ui.View()
                
                # Adicionar os botões desabilitados do jogo
                for item in self.view.children:
                    result_view.add_item(item)
                
                # Adicionar botão de lembrete
                remind_time = current_time + datetime.timedelta(minutes=5)
                reminder_button = BoxReminderButton(self.user_id, self.lang, remind_time)
                result_view.add_item(reminder_button)
                
                # Atualizar a mensagem com o resultado e o botão de lembrete
                try:
                    if not interaction.response.is_done():
                        await interaction.response.edit_message(embed=embed, view=result_view)
                    else:
                        await interaction.message.edit(embed=embed, view=result_view)
                except discord.NotFound:
                    # Interação expirada ou inválida
                    pass
                except Exception as e:
                    await log_error(f"Erro ao editar mensagem (derrota): {e}")
        except Exception as e:
            await log_error(f"Erro no callback do botão de box: {e}")
            try:
                if not interaction.response.is_done():
                    await interaction.response.send_message(
                        t('error_occurred', self.lang),
                        ephemeral=True
                    )
                else:
                    await interaction.followup.send(
                        t('error_occurred', self.lang),
                        ephemeral=True
                    )
            except discord.NotFound:
                # Interação expirada ou inválida
                pass
            except Exception as e:
                await log_error(f"Erro ao enviar mensagem de erro (box): {e}")

# View para o jogo da caixa
class BoxGameView(discord.ui.View):
    def __init__(self, user_id, lang):
        super().__init__(timeout=60)  # 1 minuto para escolher
        
        try:
            # Escolher uma caixa aleatória para ser a vencedora (1-5)
            winning_box = random.randint(1, 5)
            
            # Adicionar 5 botões (caixas)
            for i in range(1, 6):
                is_winner = (i == winning_box)
                self.add_item(BoxGameButton(i, is_winner, user_id, lang))
        except Exception as e:
            print(f"❌ Erro ao criar view do jogo da caixa: {e}")

# Classe para o botão de lembrete do jogo da caixa
class BoxReminderButton(discord.ui.Button):
    def __init__(self, user_id, lang, box_time):
        super().__init__(
            style=discord.ButtonStyle.primary,
            label=t('box_reminder_button', lang),
            emoji="⏰"
        )
        self.user_id = user_id
        self.lang = lang
        self.box_time = box_time
        
    async def callback(self, interaction):
        try:
            # Verificar se quem clicou é o dono do botão
            if interaction.user.id != self.user_id:
                try:
                    if not interaction.response.is_done():
                        await interaction.response.send_message(
                            t('not_your_button', self.lang),
                            ephemeral=True
                        )
                    else:
                        await interaction.followup.send(
                            t('not_your_button', self.lang),
                            ephemeral=True
                        )
                except discord.NotFound:
                    # Interação expirada ou inválida
                    pass
                except Exception as e:
                    await log_error(f"Erro ao responder interação (not_your_button): {e}")
                return
                
            # Calcular quando o lembrete deve ser enviado
            current_time = datetime.datetime.now()
            time_diff = (self.box_time - current_time).total_seconds()
            
            if time_diff <= 0:
                # O cooldown já acabou
                try:
                    if not interaction.response.is_done():
                        await interaction.response.send_message(
                            t('box_already_available', self.lang),
                            ephemeral=True
                        )
                    else:
                        await interaction.followup.send(
                            t('box_already_available', self.lang),
                            ephemeral=True
                        )
                except discord.NotFound:
                    # Interação expirada ou inválida
                    pass
                except Exception as e:
                    await log_error(f"Erro ao responder interação (box_already_available): {e}")
                return
                
            # Registrar o lembrete
            box_reminders[self.user_id] = self.box_time
            
            # Confirmar com o usuário
            try:
                if not interaction.response.is_done():
                    await interaction.response.send_message(
                        t('box_reminder_set', self.lang, {
                            'minutes': int(time_diff / 60)
                        }),
                        ephemeral=True
                    )
                else:
                    await interaction.followup.send(
                        t('box_reminder_set', self.lang, {
                            'minutes': int(time_diff / 60)
                        }),
                        ephemeral=True
                    )
            except discord.NotFound:
                # Interação expirada ou inválida
                pass
            except Exception as e:
                await log_error(f"Erro ao responder interação (box_reminder_set): {e}")
                return
            
            try:
                # Desativar o botão após o clique
                self.disabled = True
                await interaction.message.edit(view=self.view)
            except Exception as e:
                await log_error(f"Erro ao desabilitar botão: {e}")
            
            # Agendar o lembrete
            bot.loop.create_task(send_box_reminder(interaction.user, self.box_time, self.lang))
        except Exception as e:
            await log_error(f"Erro no callback do botão de lembrete de box: {e}")
            try:
                if not interaction.response.is_done():
                    await interaction.response.send_message(
                        t('error_occurred', self.lang),
                        ephemeral=True
                    )
                else:
                    await interaction.followup.send(
                        t('error_occurred', self.lang),
                        ephemeral=True
                    )
            except discord.NotFound:
                # Interação expirada ou inválida
                pass
            except Exception as e:
                await log_error(f"Erro ao enviar mensagem de erro (lembrete): {e}")
        

async def send_box_reminder(user, box_time, lang):
    """Função para enviar o lembrete quando o cooldown do box acabar"""
    try:
        current_time = datetime.datetime.now()
        time_diff = (box_time - current_time).total_seconds()
        
        if time_diff > 0:
            # Esperar até o tempo do lembrete
            await asyncio.sleep(time_diff)
        
        # Verificar se o usuário ainda tem o lembrete ativado
        if user.id in box_reminders and box_reminders[user.id] == box_time:
            try:
                # Enviar mensagem de lembrete via DM
                await user.send(t('box_reminder_message', lang))
                
                # Limpar o lembrete
                del box_reminders[user.id]
            except Exception as e:
                print(f"❌ Erro ao enviar lembrete de box para {user.id}: {e}")
    except Exception as e:
        await log_error(f"Erro ao processar lembrete de box: {e}")

@bot.command(name='box')
@in_trade_channel()  # Verifica se o comando está sendo usado no canal correto
async def box_command(ctx):
    """Comando para jogar o jogo da caixa e ganhar trades"""
    try:
        user_id = ctx.author.id
        # Obter idioma do usuário
        lang = get_user_language(user_id)
        
        # Verificar cooldown
        current_time = datetime.datetime.now()
        if user_id in box_cooldowns:
            last_use = box_cooldowns[user_id]
            time_diff = current_time - last_use
            
            # Verificar se já passaram 5 minutos desde o último uso
            if time_diff.total_seconds() < 300:  # 5 minutos em segundos
                minutes_left = 5 - (time_diff.total_seconds() / 60)
                
                # Criar embed para aviso de cooldown
                embed = discord.Embed(
                    title=t('box_cooldown_title', lang),
                    description=t('box_cooldown_desc', lang, {
                        'minutes': int(minutes_left),
                        'seconds': int((minutes_left % 1) * 60)
                    }),
                    color=0xff9900
                )
                
                # Criar view com o botão de lembrete
                view = BoxReminderView(user_id, lang)
                
                await ctx.send(embed=embed, view=view)
                return
        
        # Criar embed com instruções do jogo
        embed = discord.Embed(
            title=t('box_game_title', lang),
            description=t('box_game_desc', lang, {'user': ctx.author.mention}),
            color=0x3399ff
        )
        
        # Adicionar informações sobre o prêmio
        embed.add_field(
            name=t('box_game_prize_title', lang),
            value=t('box_game_prize_desc', lang),
            inline=False
        )
        
        # Criar a view com os botões do jogo
        view = BoxGameView(user_id, lang)
        
        # Enviar mensagem com o jogo
        await ctx.send(embed=embed, view=view)
    except Exception as e:
        user_id = ctx.author.id
        lang = get_user_language(user_id)
        await log_error(f"Erro no comando box: {e}")
        await ctx.send(t('command_error', lang))

@bot.command(name='resetbox')
@commands.has_permissions(administrator=True)  # Restringe apenas para administradores
async def resetbox_command(ctx, member: discord.Member):
    """Comando para administradores resetarem o cooldown do box de um usuário"""
    # Obter idioma do usuário
    lang = get_user_language(ctx.author.id)
    
    try:
        # Verificar se o membro foi especificado
        if not member:
            await ctx.send(t('resetbox_no_member', lang))
            return
        
        # Remover o usuário do dicionário de cooldown
        if member.id in box_cooldowns:
            del box_cooldowns[member.id]
            
            # Remover qualquer lembrete pendente
            if member.id in box_reminders:
                del box_reminders[member.id]
            
            # Atualizar no MongoDB
            if db.is_connected():
                db.remove_box_cooldown(member.id)
            
            await ctx.send(t('resetbox_success', lang, {'user': member.display_name}))
        else:
            await ctx.send(t('resetbox_not_on_cooldown', lang, {'user': member.display_name}))
    except Exception as e:
        await log_error(f"Erro no comando resetbox: {e}")
        await ctx.send(t('command_error', lang))

@bot.command(name='ajuda')
async def help_command(ctx):
    """Exibe ajuda sobre os comandos do bot"""
    try:
        # Obter idioma do usuário
        lang = get_user_language(ctx.author.id)
        
        if ctx.author.guild_permissions.administrator:
            # Se for admin, mostra também a ajuda de admin
            await adminhelp_command(ctx)
        
        embed = discord.Embed(
            title=t('embed_help_title', lang),
            description=t('embed_help_desc', lang),
            color=0xffbb00
        )
        
        embed.add_field(
            name="!listtrades", 
            value=t('help_listtrades', lang), 
            inline=False
        )
        
        embed.add_field(
            name="!claimtrade", 
            value=t('help_claimtrade', lang), 
            inline=False
        )
        
        embed.add_field(
            name="!usetrade [quantidade]", 
            value=t('help_usetrade', lang),
            inline=False
        )
        
        embed.add_field(
            name="!slot", 
            value=t('help_slot', lang), 
            inline=False
        )
        
        embed.add_field(
            name="!box", 
            value=t('help_box', lang), 
            inline=False
        )
        
        embed.add_field(
            name="!abort [código]", 
            value=t('help_abort', lang), 
            inline=False
        )
        
        embed.add_field(
            name="!tradeshistory", 
            value=t('help_tradeshistory', lang), 
            inline=False
        )
        
        embed.add_field(
            name="!checktrademember [@usuário]", 
            value=t('help_checktrademember', lang), 
            inline=False
        )
        
        embed.add_field(
            name="!ajuda", 
            value=t('help_help', lang), 
            inline=False
        )
        
        embed.add_field(
            name="!lang [pt/en/es]", 
            value=t('help_lang', lang), 
            inline=False
        )
        
        await ctx.send(embed=embed)
    except Exception as e:
        user_id = ctx.author.id
        lang = get_user_language(user_id)
        await log_error(f"Erro no comando help: {e}")
        await ctx.send(t('command_error', lang))

@bot.command(name='adminhelp')
@commands.has_permissions(administrator=True)  # Restringe apenas para administradores
async def adminhelp_command(ctx):
    """Exibe ajuda sobre os comandos de administrador"""
    try:
        # Obter idioma do usuário
        lang = get_user_language(ctx.author.id)
        
        embed = discord.Embed(
            title=t('embed_admin_help', lang),
            description=t('embed_admin_help_desc', lang),
            color=0xff5500
        )
        
        embed.add_field(
            name="!trade [quantidade] [tempo_expiração]", 
            value=t('help_trade', lang), 
            inline=False
        )
        
        embed.add_field(
            name="!timemode [duração] [tempo_expiração]", 
            value=t('help_timemode', lang), 
            inline=False
        )
        
        embed.add_field(
            name="!status [código]", 
            value=t('help_status', lang), 
            inline=False
        )
        
        embed.add_field(
            name="!givetrade [@usuário] [quantidade]", 
            value=t('help_givetrade', lang), 
            inline=False
        )
        
        embed.add_field(
            name="!activecodes", 
            value=t('help_activecodes', lang), 
            inline=False
        )
        
        embed.add_field(
            name="!resetclaim [@usuário]", 
            value=t('help_resetclaim', lang), 
            inline=False
        )
        
        embed.add_field(
            name="!resetslot [@usuário]", 
            value=t('help_resetslot', lang), 
            inline=False
        )
        
        embed.add_field(
            name="!resetbox [@usuário]", 
            value=t('help_resetbox', lang), 
            inline=False
        )
        
        embed.add_field(
            name="!stats [período]", 
            value=t('help_stats', lang), 
            inline=False
        )
        
        embed.add_field(
            name="!resetuser [@usuário]", 
            value=t('Resetar código de trade ativo de um usuário'), 
            inline=False
        )
        
        await ctx.send(embed=embed)
    except Exception as e:
        user_id = ctx.author.id
        lang = get_user_language(user_id)
        await log_error(f"Erro no comando adminhelp: {e}")
        await ctx.send(t('command_error', lang))

@bot.command(name='helpdb')
@commands.has_permissions(administrator=True)  # Restringe apenas para administradores
async def helpdb_command(ctx):
    """Exibe informações sobre o status da conexão com o banco de dados"""
    try:
        # Obter idioma do usuário
        lang = get_user_language(ctx.author.id)
        
        embed = discord.Embed(
            title=t('embed_db_status', lang),
            color=0x0088ff
        )
        
        if db.is_connected():
            embed.description = t('db_connected', lang)
            embed.add_field(
                name="Informações", 
                value=t('db_info', lang), 
                inline=False
            )
            
            # Adicionar estatísticas
            user_trades_count = len(user_trades)
            daily_cooldown_count = len(daily_claim_cooldown)
            active_trades_count = len(active_trades)
            active_users_count = len(users_with_active_trade)
            
            embed.add_field(
                name="Estatísticas", 
                value=t('db_stats', lang, {
                    'users': user_trades_count,
                    'cooldowns': daily_cooldown_count,
                    'active': active_trades_count,
                    'in_progress': active_users_count
                }),
                inline=False
            )
        else:
            embed.description = t('db_disconnected', lang)
            embed.add_field(
                name="Atenção", 
                value=t('db_memory_warning', lang), 
                inline=False
            )
            embed.add_field(
                name="Solução", 
                value=t('db_solution', lang), 
                inline=False
            )
        
        await ctx.send(embed=embed)
    except Exception as e:
        user_id = ctx.author.id
        lang = get_user_language(user_id)
        await log_error(f"Erro no comando helpdb: {e}")
        await ctx.send(t('command_error', lang))

async def process_trade_with_dm(ctx, code, dm_message, trades_amount):
    """Processa um trade em segundo plano e envia atualizações via DM"""
    try:
        # Obter idioma do usuário
        lang = get_user_language(ctx.author.id)
        
        # Obter informações do código
        code_info = active_trades[code]
        expire_minutes = code_info.get('expire_minutes', 60)
        
        # Atualizar status
        code_info['status'] = 'processing'
        
        # Atualizar no MongoDB
        if db.is_connected():
            db.update_active_trade_status(code, 'processing')
        
        await dm_message.edit(content=t('trade_processing', lang, {'amount': trades_amount, 'code': code}))
        
        # Adquirir semáforo para limitar trades simultâneos
        async with trade_semaphore:
            try:
                # Executar o script main.py com os parâmetros apropriados para trades específicos
                returncode, stdout, stderr = await run_trade_process(
                    code, 
                    expire_minutes,
                    'trades',
                    None,
                    trades_amount  # Passando a quantidade de trades
                )
                
                # Verificar se o processo foi bem-sucedido
                if returncode == 0:
                    code_info['status'] = 'completed'
                    
                    # Atualizar no MongoDB
                    if db.is_connected():
                        db.update_active_trade_status(code, 'completed')
                    
                    # Criar embed com o resultado
                    embed = discord.Embed(
                        title=t('trade_success', lang),
                        description=t('trade_success_desc', lang, {'amount': trades_amount}),
                        color=0x00ff00
                    )
                    embed.add_field(name="Código", value=f"**{code}**", inline=False)
                    
                    embed.add_field(
                        name=t('trade_completed', lang), 
                        value=t('trade_more_info', lang), 
                        inline=False
                    )
                    embed.add_field(
                        name=t('trade_by', lang), 
                        value=f"Math", 
                        inline=False
                    )
                    
                    # Adicionar log de saída resumido como footer
                    log_lines = stdout.splitlines()
                    if log_lines:
                        important_lines = [line for line in log_lines if "[SUCESSO]" in line or "[OK]" in line]
                        if important_lines:
                            summary = important_lines[-1]  # Última linha importante
                            embed.set_footer(text=summary)
                    
                    # Send completion embed via DM
                    await dm_message.edit(content=None, embed=embed)
                    
                    # Also send a simpler public confirmation (without the code)
                    public_embed = discord.Embed(
                        title=t('trade_success', lang),
                        description=t('trade_success_public', lang, {'mention': ctx.author.mention}),
                        color=0x00ff00
                    )
                    public_embed.add_field(
                        name="Detalhes", 
                        value=t('trade_details_sent', lang), 
                        inline=False
                    )
                    await ctx.send(embed=public_embed)
                    
                    # Disparar evento de trade completado
                    bot.dispatch('trade_completed', ctx.author.id, code)
                    
                else:
                    code_info['status'] = 'failed'
                    
                    # Atualizar no MongoDB
                    if db.is_connected():
                        db.update_active_trade_status(code, 'failed')
                    
                    # Criar embed com o erro
                    embed = discord.Embed(
                        title=t('trade_error', lang),
                        description=t('trade_error_desc', lang, {'code': code}),
                        color=0xff0000
                    )
                    
                    # Adicionar detalhes do erro
                    error_lines = stderr.splitlines()
                    if error_lines:
                        error_message = error_lines[-1]  # Última linha de erro
                        embed.add_field(name="Erro", value=error_message, inline=False)
                    
                    # Send error via DM
                    await dm_message.edit(content=None, embed=embed)
                    
                    # Also notify about the error in public (without the code)
                    await ctx.send(t('trade_error_public', lang, {'mention': ctx.author.mention}))
                    
            except Exception as e:
                code_info['status'] = 'failed'
                
                # Atualizar no MongoDB
                if db.is_connected():
                    db.update_active_trade_status(code, 'failed')
                
                # Send error via DM
                await dm_message.edit(content=f"❌ Erro ao processar trade: {str(e)}")
                
                # Also notify about the error in public
                await ctx.send(t('trade_error_public', lang, {'mention': ctx.author.mention}))
    except Exception as e:
        await log_error(f"Erro em process_trade_with_dm: {e}")
        try:
            await dm_message.edit(content=f"❌ Erro ao processar trade: {str(e)}")
        except:
            pass

# Update your process_trade variable to use the new DM function
process_trade = process_trade_with_dm   # You can keep this for admin commands

# Limpar trades ativos de um usuário quando um trade é concluído
@bot.event
async def on_trade_completed(user_id, code):
    """Evento chamado quando um trade é concluído"""
    try:
        if user_id in users_with_active_trade and users_with_active_trade[user_id] == code:
            del users_with_active_trade[user_id]
            
            # Atualizar no MongoDB
            if db.is_connected():
                db.remove_user_active_trade(user_id)
    except Exception as e:
        await log_error(f"Erro no evento on_trade_completed: {e}")

# Adicionar funções de tratamento de erros para explicar quando comandos requerem permissões de admin
@trade_command.error
@timemode_command.error
@status_command.error
@givetrade_command.error
@resetslot_command.error
@resetbox_command.error
@adminhelp_command.error
@helpdb_command.error
async def admin_command_error(ctx, error):
    try:
        # Obter idioma do usuário
        lang = get_user_language(ctx.author.id)
        
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(t('admin_only', lang))
        else:
            await log_error(f"Erro em comando de admin ({ctx.command}): {error}")
    except Exception as e:
        await log_error(f"Erro ao tratar erro de comando de admin: {e}")

# Adicionar função de tratamento de erros para explicar quando comandos devem ser usados no canal correto
@listtrades_command.error
@claimtrade_command.error
@usetrade_command.error
@slot_command.error
@box_command.error
async def channel_command_error(ctx, error):
    try:
        # Obter idioma do usuário
        lang = get_user_language(ctx.author.id)
        
        if isinstance(error, commands.CheckFailure):
            if TRADE_CHANNEL_ID:
                trade_channel = bot.get_channel(int(TRADE_CHANNEL_ID))
                if trade_channel:
                    await ctx.send(t('wrong_channel', lang, {'channel': trade_channel.mention}))
                else:
                    await ctx.send(t('command_unavailable', lang))
            else:
                await ctx.send(t('command_unavailable', lang))
        else:
            await log_error(f"Erro em comando de canal ({ctx.command}): {error}")
    except Exception as e:
        await log_error(f"Erro ao tratar erro de comando de canal: {e}")

async def cleanup_expired_trades():
    """Remove trades expirados do dicionário"""
    while True:
        try:
            current_time = datetime.datetime.now()
            codes_to_remove = []
            
            # Se o MongoDB estiver conectado, usar sua função de limpeza
            if db.is_connected():
                deleted_count = db.delete_expired_trades()
                if deleted_count > 0:
                    print(f"🧹 {deleted_count} trades expirados removidos do MongoDB")
                    
                # Atualizar dicionários locais
                active_trades_data = db.get_all_active_trades()
                if active_trades_data:
                    global active_trades
                    active_trades = active_trades_data
            
            # Cleanup em memória
            for code, info in active_trades.items():
                # Usar o tempo de expiração específico para cada código
                expire_minutes = info.get('expire_minutes', 30)
                if (current_time - info['timestamp']).total_seconds() > expire_minutes * 60:
                    codes_to_remove.append(code)
                    
                    # Se o usuário tem este código como ativo, remove do dicionário de usuários com trades ativos
                    user_id = info.get('user_id')
                    if user_id in users_with_active_trade and users_with_active_trade[user_id] == code:
                        del users_with_active_trade[user_id]
                        
                        # Atualizar no MongoDB
                        if db.is_connected():
                            db.remove_user_active_trade(user_id)
            
            for code in codes_to_remove:
                del active_trades[code]
                
                # Remover do MongoDB
                if db.is_connected():
                    db.delete_active_trade(code)
        except Exception as e:
            await log_error(f"Erro na tarefa de limpeza de trades expirados: {e}")
            
        await asyncio.sleep(60)  # Verificar a cada minuto

@bot.event
async def on_ready():
    """Evento disparado quando o bot está pronto"""
    try:
        print(f'Bot conectado como {bot.user.name}')
        activity = discord.Activity(type=discord.ActivityType.watching, name="trades | !help")
        await bot.change_presence(activity=activity)

        await log_error("Bot iniciado com sucesso")
        
        # Carregar dados do MongoDB
        load_data_from_mongodb()
        
        # Iniciar tarefa de sincronização com MongoDB
        bot.loop.create_task(sync_data_to_mongodb())
        
        # Iniciar tarefa de limpeza de trades expirados
        bot.loop.create_task(cleanup_expired_trades())
    except Exception as e:
        await log_error(f"Erro no evento on_ready: {e}")

@bot.command(name='resetuser')
@commands.has_permissions(administrator=True)  # Restringe apenas para administradores
async def resetuser_command(ctx, member: discord.Member):
    """Comando para administradores resetarem o status de trade ativo de um usuário"""
    # Obter idioma do usuário
    lang = get_user_language(ctx.author.id)
    
    try:
        # Verificar se o membro foi especificado
        if not member:
            await ctx.send(t('resetuser_no_member', lang))
            return
        
        # Remover o usuário do dicionário de usuários com trades ativos
        if member.id in users_with_active_trade:
            active_code = users_with_active_trade[member.id]
            del users_with_active_trade[member.id]
            
            # Atualizar no MongoDB
            if db.is_connected():
                db.remove_user_active_trade(member.id)
            
            # Se o código existir nos trades ativos, também marca como falhou
            if active_code in active_trades:
                active_trades[active_code]['status'] = 'failed'
                
                # Atualizar no MongoDB
                if db.is_connected():
                    db.update_active_trade_status(active_code, 'failed')
            
            await ctx.send(t('resetuser_success', lang, {'user': member.display_name, 'code': active_code}))
        else:
            await ctx.send(t('resetuser_no_active_trade', lang, {'user': member.display_name}))
    except Exception as e:
        await log_error(f"Erro no comando resetuser: {e}")
        await ctx.send(t('command_error', lang))

@resetuser_command.error
async def resetuser_error(ctx, error):
    try:
        # Obter idioma do usuário
        lang = get_user_language(ctx.author.id)
        
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(t('admin_only', lang))
        else:
            await log_error(f"Erro em comando resetuser: {error}")
    except Exception as e:
        await log_error(f"Erro ao tratar erro do comando resetuser: {e}")

# Executar o bot com o token do Discord
if __name__ == "__main__":
    if not TOKEN:
        print("⚠️ DISCORD_TOKEN não encontrado no arquivo .env")
        exit(1)
    
    # Verificar se TRADE_CHANNEL_ID está configurado
    if not TRADE_CHANNEL_ID:
        print("⚠️ TRADE_CHANNEL_ID não está configurado. Comandos de usuário funcionarão em qualquer canal.")
    
    # Definir o idioma padrão do bot
    print(f"🌐 Idioma padrão do bot: {DEFAULT_LANGUAGE}")
    keep_alive()
    bot.run(TOKEN)
