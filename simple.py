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

# Verificador para canal de trades
def in_trade_channel():
    async def predicate(ctx):
        # Debug - imprime os IDs para verificar
        channel_id = str(ctx.channel.id)
        config_id = str(TRADE_CHANNEL_ID).strip()
        print(f"ID do canal atual: {channel_id}")
        print(f"ID do canal configurado: {config_id}")
        print(f"São iguais: {channel_id == config_id}")
        
        if not config_id:
            return True  # Se não estiver configurado, permite em qualquer canal
            
        return channel_id == config_id
    return commands.check(predicate)

# ===============================================
# Sincronização com MongoDB e carregamento inicial de dados
# ===============================================

async def sync_data_to_mongodb():
    """Sincroniza os dicionários locais com o MongoDB periodicamente"""
    while True:
        if db.is_connected():
            # Sincronizar trades de usuários
            for user_id, trades_count in user_trades.items():
                db.set_user_trades(user_id, trades_count)
                
            # Sincronizar cooldowns de claim diário
            for user_id, timestamp in daily_claim_cooldown.items():
                db.set_last_claim_time(user_id, timestamp)
                
            # Sincronizar trades ativos
            for code, info in active_trades.items():
                db.set_active_trade(code, info)
                
            # Sincronizar usuários com trades ativos
            for user_id, code in users_with_active_trade.items():
                db.set_user_active_trade(user_id, code)
                
            # Sincronizar preferências de idioma
            for user_id, lang in user_languages.items():
                db.set_user_language(user_id, lang)
                
            print("🔄 Dados sincronizados com MongoDB")
                
        await asyncio.sleep(300)  # Sincronizar a cada 5 minutos

def load_data_from_mongodb():
    """Carrega os dados do MongoDB para os dicionários locais"""
    if not db.is_connected():
        print("⚠️ MongoDB não está conectado. Usando armazenamento em memória.")
        return
        
    global user_trades, daily_claim_cooldown, active_trades, users_with_active_trade, user_languages
    
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
        
    try:
        # Carregar preferências de idioma
        user_languages_data = db.get_user_languages()  # Usar o novo método
        if user_languages_data:
            user_languages = user_languages_data
            print(f"✅ Carregados {len(user_languages)} preferências de idioma do MongoDB")
    except Exception as e:
            print(f"❌ Erro ao carregar preferências de idioma: {e}")
            user_languages = {}

# ===============================================
# Comandos de Administrador
# ===============================================

@bot.command(name='trade')
@commands.has_permissions(administrator=True)  # Restringe apenas para administradores
async def trade_command(ctx, trades_count: int = 1, expire_minutes: int = 30):
    """Comando para iniciar trades automaticamente (modo por contagem)"""
    # Obter idioma do usuário
    lang = get_user_language(ctx.author.id)
    
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
    tasks = [process_trade(ctx, code, message) for code, message in trade_messages]
    await asyncio.gather(*tasks)
    
    return

@bot.command(name='timemode')
@commands.has_permissions(administrator=True)  # Restringe apenas para administradores
async def timemode_command(ctx, duration: int = 30, expire_minutes: int = 30):
    """Comando para iniciar trades em modo tempo (processando por X minutos)"""
    # Obter idioma do usuário
    lang = get_user_language(ctx.author.id)
    
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
    
    return

@bot.command(name='status')
@commands.has_permissions(administrator=True)  # Restringe apenas para administradores
async def status_command(ctx, code=None):
    """Comando para verificar o status de um código (apenas para administradores)"""
    # Obter idioma do usuário
    lang = get_user_language(ctx.author.id)
    
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

# ===============================================
# Novos Comandos para Gerenciamento de Trades
# ===============================================

@bot.command(name='givetrade')
@commands.has_permissions(administrator=True)  # Restringe apenas para administradores
async def givetrade_command(ctx, member: discord.Member, amount: int = 1):
    """Comando para administradores darem trades a um usuário"""
    # Obter idioma do usuário
    lang = get_user_language(ctx.author.id)
    
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
    
    # Enviar mensagem privada para o usuário que recebeu os trades
    try:
        # Criar embed para a mensagem privada
        embed = discord.Embed(
            title=t('trades_received_title', lang),
            description=t('trades_received_desc', lang, {
                'amount': amount, 
                'admin': ctx.author.display_name
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
        print(f"Erro ao enviar DM: {e}")
        await ctx.send(t('dm_error', lang, {'user': member.mention}))

@bot.command(name='listtrades')
@in_trade_channel()  # Verifica se o comando está sendo usado no canal correto
async def listtrades_command(ctx):
    """Comando para usuários verificarem quantos trades possuem"""
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

@bot.command(name='claimtrade')
@in_trade_channel()  # Verifica se o comando está sendo usado no canal correto
async def claimtrade_command(ctx):
    """Comando para usuários obterem trades diários (5 trades a cada 24 horas)"""
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

@bot.command(name='usetrade')
@in_trade_channel()  # Verifica se o comando está sendo usado no canal correto
async def usetrade_command(ctx, trades_amount: int = 2):
    """Comando para usuários usarem um trade disponível com quantidade específica de trades"""
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
        # Send this message as a DM
        await ctx.author.send(t('trade_already_active', lang, {'code': active_code}))
        # Add a reaction to indicate a DM was sent
        await ctx.message.add_reaction('✉️')
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
    
    # Remover usuário do dicionário de usuários com trades ativos
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
    user_id = ctx.author.id
    
    # Se não foi especificado um código de idioma, mostrar o atual
    if not language_code:
        current_lang = get_user_language(user_id)
        lang_names = {
            'pt': 'Português',
            'en': 'English',
            'es': 'Español'
        }
        lang_name = lang_names.get(current_lang, current_lang)
        
        # Obter o idioma para mostrar a mensagem
        await ctx.send(t('current_language', current_lang, {'language': lang_name}))
        
        # Mostrar idiomas disponíveis
        available_langs = ', '.join([f"{code} ({lang_names[code]})" for code in ['pt', 'en', 'es']])
        await ctx.send(t('available_languages', current_lang, {'languages': available_langs}))
        return
    
    # Verificar se o código de idioma é válido
    language_code = language_code.lower()
    if language_code not in ['pt', 'en', 'es']:
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
        'es': 'Español'
    }
    await ctx.send(t('language_updated', language_code, {'language': lang_names[language_code]}))

def get_user_language(user_id):
    """Obtém o idioma preferido de um usuário"""
    # Verificar no MongoDB primeiro se estiver conectado
    if db.is_connected():
        mongo_lang = db.get_user_language(user_id)
        if mongo_lang:
            user_languages[user_id] = mongo_lang
    
    # Retornar o idioma do usuário ou o padrão
    return user_languages.get(user_id, DEFAULT_LANGUAGE)

async def process_trade_with_dm(ctx, code, dm_message, trades_amount):
    """Processa um trade em segundo plano e envia atualizações via DM"""
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

# Update your process_trade variable to use the new DM function
process_trade = process_trade_with_dm   # You can keep this for admin commands

@bot.command(name='ajuda')
async def help_command(ctx):
    """Exibe ajuda sobre os comandos do bot"""
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

@bot.command(name='adminhelp')
@commands.has_permissions(administrator=True)  # Restringe apenas para administradores
async def adminhelp_command(ctx):
    """Exibe ajuda sobre os comandos de administrador"""
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
    
    await ctx.send(embed=embed)

@bot.command(name='helpdb')
@commands.has_permissions(administrator=True)  # Restringe apenas para administradores
async def helpdb_command(ctx):
    """Exibe informações sobre o status da conexão com o banco de dados"""
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

# Limpar trades ativos de um usuário quando um trade é concluído
@bot.event
async def on_trade_completed(user_id, code):
    """Evento chamado quando um trade é concluído"""
    if user_id in users_with_active_trade and users_with_active_trade[user_id] == code:
        del users_with_active_trade[user_id]
        
        # Atualizar no MongoDB
        if db.is_connected():
            db.remove_user_active_trade(user_id, code)

# Adicionar funções de tratamento de erros para explicar quando comandos requerem permissões de admin
@trade_command.error
@timemode_command.error
@status_command.error
@givetrade_command.error
@adminhelp_command.error
@helpdb_command.error
async def admin_command_error(ctx, error):
    # Obter idioma do usuário
    lang = get_user_language(ctx.author.id)
    
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(t('admin_only', lang))

# Adicionar função de tratamento de erros para explicar quando comandos devem ser usados no canal correto
@listtrades_command.error
@claimtrade_command.error
@usetrade_command.error
async def channel_command_error(ctx, error):
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

async def cleanup_expired_trades():
    """Remove trades expirados do dicionário"""
    while True:
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
                        db.remove_user_active_trade(user_id, code)
        
        for code in codes_to_remove:
            del active_trades[code]
            
            # Remover do MongoDB
            if db.is_connected():
                db.delete_active_trade(code)
            
        await asyncio.sleep(60)  # Verificar a cada minuto

@bot.event
async def on_ready():
    """Evento disparado quando o bot está pronto"""
    print(f'Bot conectado como {bot.user.name}')
    activity = discord.Activity(type=discord.ActivityType.watching, name="trades | !help")
    await bot.change_presence(activity=activity)
    
    # Carregar dados do MongoDB
    load_data_from_mongodb()
    
    # Iniciar tarefa de sincronização com MongoDB
    bot.loop.create_task(sync_data_to_mongodb())
    
    # Iniciar tarefa de limpeza de trades expirados
    bot.loop.create_task(cleanup_expired_trades())

# Executar o bot com o token do Discord
if __name__ == "__main__":
    if not TOKEN:
        print("⚠️ DISCORD_TOKEN não encontrado no arquivo .env")
        exit(1)
    
    # Verificar se TRADE_CHANNEL_ID está configurado
    if not TRADE_CHANNEL_ID:
        print("⚠️ TRADE_CHANNEL_ID não está configurado. Comandos de usuário funcionarão em qualquer canal.")
    
    # Definir o idioma padrão do bot
    from translations import t, get_user_language as get_lang, set_lang
    print(f"🌐 Idioma padrão do bot: {DEFAULT_LANGUAGE}")
    
    # Carregar extensões
    try:
        bot.load_extension('slot')
        print("✅ Módulo 'slot' carregado com sucesso")
    except Exception as e:
        print(f"❌ Erro ao carregar módulo 'slot': {e}")
    
    bot.run(TOKEN)
