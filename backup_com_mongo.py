import discord
from discord.ext import commands
import random
import os
import datetime
import subprocess
import asyncio
from dotenv import load_dotenv
from database import Database  # Importar a classe de banco de dados

# Carregar variáveis de ambiente
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
TRADE_CHANNEL_ID = os.getenv('TRADE_CHANNEL_ID', '1362465656263544904')  # ID do canal específico para trades

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
                
            print("🔄 Dados sincronizados com MongoDB")
                
        await asyncio.sleep(300)  # Sincronizar a cada 5 minutos

def load_data_from_mongodb():
    """Carrega os dados do MongoDB para os dicionários locais"""
    if not db.is_connected():
        print("⚠️ MongoDB não está conectado. Usando armazenamento em memória.")
        return
        
    global user_trades, daily_claim_cooldown, active_trades, users_with_active_trade
    
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

# ===============================================
# Comandos de Administrador
# ===============================================

@bot.command(name='trade')
@commands.has_permissions(administrator=True)  # Restringe apenas para administradores
async def trade_command(ctx, trades_count: int = 1, expire_minutes: int = 30):
    """Comando para iniciar trades automaticamente (modo por contagem)"""
    # Validar quantidade de trades
    if trades_count < 1 or trades_count > 10:
        await ctx.send("⚠️ Você pode solicitar entre 1 e 10 trades.")
        return
    
    # Validar tempo de expiração
    if expire_minutes < 1 or expire_minutes > 120:
        await ctx.send("⚠️ O tempo de expiração deve estar entre 1 e 120 minutos.")
        return
    
    # Verificar o número de trades ativos do usuário
    user_trades_active = [code for code, info in active_trades.items() if info['user_id'] == ctx.author.id]
    if len(user_trades_active) + trades_count > 3:  # Limite de 3 trades ativos por usuário
        await ctx.send(f"⚠️ Você só pode ter até 3 trades ativos. Você já tem {len(user_trades_active)} trade(s).")
        return
    
    # Verificar se há trades simultâneos disponíveis
    if not trade_semaphore.locked() and trade_semaphore._value <= 0:
        await ctx.send("⚠️ O sistema está processando muitos trades no momento. Por favor, tente novamente em alguns minutos.")
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
        initial_message = await ctx.send(f"🔄 Gerando código de trade... Código: **{code}** (expira em {expire_minutes} minutos)")
        trade_messages.append((code, initial_message))
    
    # Processar trades em paralelo
    tasks = [process_trade(ctx, code, message) for code, message in trade_messages]
    await asyncio.gather(*tasks)
    
    return

@bot.command(name='timemode')
@commands.has_permissions(administrator=True)  # Restringe apenas para administradores
async def timemode_command(ctx, duration: int = 30, expire_minutes: int = 30):
    """Comando para iniciar trades em modo tempo (processando por X minutos)"""
    # Validar duração
    if duration < 1 or duration > 120:
        await ctx.send("⚠️ A duração do processamento deve estar entre 1 e 120 minutos.")
        return
    
    # Validar tempo de expiração
    if expire_minutes < 1 or expire_minutes > 120:
        await ctx.send("⚠️ O tempo de expiração deve estar entre 1 e 120 minutos.")
        return
    
    # Verificar o número de trades ativos do usuário
    user_trades_active = [code for code, info in active_trades.items() if info['user_id'] == ctx.author.id]
    if len(user_trades_active) >= 3:  # Limite de 3 trades ativos por usuário
        await ctx.send(f"⚠️ Você só pode ter até 3 trades ativos. Você já tem {len(user_trades_active)} trade(s).")
        return
    
    # Verificar se há trades simultâneos disponíveis
    if not trade_semaphore.locked() and trade_semaphore._value <= 0:
        await ctx.send("⚠️ O sistema está processando muitos trades no momento. Por favor, tente novamente em alguns minutos.")
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
    initial_message = await ctx.send(f"🔄 Iniciando modo tempo com código: **{code}** | Processando trades por {duration} minutos (expira em {expire_minutes} min)")
    
    # Processar o trade em modo tempo
    await process_trade(ctx, code, initial_message)
    
    return

@bot.command(name='status')
@commands.has_permissions(administrator=True)  # Restringe apenas para administradores
async def status_command(ctx, code=None):
    """Comando para verificar o status de um código (apenas para administradores)"""
    if not code:
        # Procurar códigos ativos do usuário
        user_trades_active = [
            (code, info) for code, info in active_trades.items() 
            if info['user_id'] == ctx.author.id
        ]
        
        if not user_trades_active:
            await ctx.send("❌ Você não tem trades ativos no momento.")
            return
        
        embed = discord.Embed(
            title="🔍 Seus Trades Ativos",
            description=f"Você tem {len(user_trades_active)} trade(s) ativo(s):",
            color=0x0088ff
        )
        
        for code, info in user_trades_active:
            time_diff = datetime.datetime.now() - info['timestamp']
            # Usar o tempo de expiração específico
            expire_minutes = info.get('expire_minutes', 30)
            minutes_left = max(0, expire_minutes - int(time_diff.total_seconds() / 60))
            
            status_text = info['status']
            if status_text == 'pending':
                status_text = "Aguardando processamento"
            elif status_text == 'processing':
                status_text = "Em processamento"
            elif status_text == 'completed':
                status_text = "✅ Concluído com sucesso"
            elif status_text == 'failed':
                status_text = "❌ Falha no processamento"
            
            mode_text = "Modo tempo" if info.get('mode') == 'time' else "Modo trades"
            
            embed.add_field(
                name=f"Código: {code}",
                value=f"Status: {status_text}\nTempo restante: {minutes_left} minutos\nModo: {mode_text}",
                inline=False
            )
        
        await ctx.send(embed=embed)
        return
    
    # Verificar um código específico
    if code not in active_trades:
        await ctx.send(f"❌ Código não encontrado: {code}")
        return
    
    code_info = active_trades[code]
    
    # Verificar se o usuário é o dono do código ou um administrador
    if code_info['user_id'] != ctx.author.id and not ctx.author.guild_permissions.administrator:
        await ctx.send("❌ Este código não pertence a você.")
        return
    
    # Verificar status do código
    time_diff = datetime.datetime.now() - code_info['timestamp']
    # Usar o tempo de expiração específico
    expire_minutes = code_info.get('expire_minutes', 30)
    minutes_left = max(0, expire_minutes - int(time_diff.total_seconds() / 60))
    
    status_text = code_info['status']
    if status_text == 'pending':
        status_text = "Aguardando processamento"
    elif status_text == 'processing':
        status_text = "Em processamento"
    elif status_text == 'completed':
        status_text = "✅ Concluído com sucesso"
    elif status_text == 'failed':
        status_text = "❌ Falha no processamento"
    
    mode_text = "Modo tempo" if code_info.get('mode') == 'time' else "Modo trades"
    duration = code_info.get('duration', None)
    
    embed = discord.Embed(
        title=f"🔍 Status do Trade: {code}",
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
    if amount < 1 or amount > 100:
        await ctx.send("⚠️ A quantidade de trades deve estar entre 1 e 100.")
        return
    
    # Inicializa o dicionário do usuário se não existir
    if member.id not in user_trades:
        user_trades[member.id] = 0
    
    # Adiciona os trades ao usuário
    user_trades[member.id] += amount
    
    # Atualizar no MongoDB
    if db.is_connected():
        db.increment_user_trades(member.id, amount)
    
    await ctx.send(f"✅ {amount} trade(s) adicionado(s) para {member.display_name}. Total atual: **{user_trades[member.id]}**")

@bot.command(name='listtrades')
@in_trade_channel()  # Verifica se o comando está sendo usado no canal correto
async def listtrades_command(ctx):
    """Comando para usuários verificarem quantos trades possuem"""
    user_id = ctx.author.id
    
    # Verificar no MongoDB primeiro se estiver conectado
    if db.is_connected():
        mongo_trades = db.get_user_trades(user_id)
        # Atualizar o dicionário local se necessário
        if user_id not in user_trades or user_trades[user_id] != mongo_trades:
            user_trades[user_id] = mongo_trades
    
    if user_id not in user_trades or user_trades[user_id] <= 0:
        await ctx.send(f"❌ Você não possui trades disponíveis. Use `!claimtrade` para obter trades diários ou peça a um administrador.")
        return
    
    await ctx.send(f"🎮 Você possui **{user_trades[user_id]}** trade(s) disponível(is).")

@bot.command(name='claimtrade')
@in_trade_channel()  # Verifica se o comando está sendo usado no canal correto
async def claimtrade_command(ctx):
    """Comando para usuários obterem trades diários (5 trades a cada 24 horas)"""
    user_id = ctx.author.id
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
            await ctx.send(f"⏰ Você já recebeu seus trades diários. Aguarde **{int(hours_left)} horas e {int((hours_left % 1) * 60)} minutos** para receber novamente.")
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
    
    await ctx.send(f"🎁 Você recebeu **5 trades diários**! Agora você possui **{user_trades[user_id]}** trade(s).")

@bot.command(name='usetrade')
@in_trade_channel()  # Verifica se o comando está sendo usado no canal correto
async def usetrade_command(ctx, trades_amount: int = 2):
    """Comando para usuários usarem um trade disponível com quantidade específica de trades"""
    user_id = ctx.author.id
    
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
        await ctx.author.send(f"⚠️ Você já possui um trade ativo com o código **{active_code}**. Aguarde até que ele seja concluído antes de usar outro trade.")
        # Add a reaction to indicate a DM was sent
        await ctx.message.add_reaction('✉️')
        return
    
    # Validar quantidade de trades
    if trades_amount < 1 or trades_amount > 10:
        await ctx.send("⚠️ A quantidade de trades deve estar entre 1 e 10.")
        return
    
    # Verifica se o usuário tem trades suficientes para a quantidade solicitada
    if user_id not in user_trades or user_trades[user_id] <= 0:
        await ctx.send("❌ Você não possui trades disponíveis. Use `!claimtrade` para obter trades diários ou peça a um administrador.")
        return
    
    # Verifica se o usuário tem trades suficientes para a quantidade solicitada
    if user_trades[user_id] < trades_amount:
        await ctx.send(f"❌ Você não possui trades suficientes. Você tem {user_trades[user_id]} trade(s) disponível(is), mas solicitou {trades_amount}.")
        return
    
    # Verificar se há trades simultâneos disponíveis
    if not trade_semaphore.locked() and trade_semaphore._value <= 0:
        await ctx.send("⚠️ O sistema está processando muitos trades no momento. Por favor, tente novamente em alguns minutos.")
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
    await ctx.send(f"🔄 Gerando um trade com {trades_amount} trocas para {ctx.author.mention}... Detalhes enviados por mensagem privada.")
    
    # Send the sensitive code information via DM
    dm_message = await ctx.author.send(f"🔄 Gerando código de trade... Código: **{code}** (expira em {expire_minutes} minutos, quantidade: {trades_amount} trades)")
    
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
    await ctx.author.send(f"ℹ️ Trade utilizado! Você ainda possui **{user_trades[user_id]}** trade(s) disponível(is).")
    
    # Remover usuário do dicionário de usuários com trades ativos
    if user_id in users_with_active_trade:
        del users_with_active_trade[user_id]
        
        # Atualizar no MongoDB
        if db.is_connected():
            db.remove_user_active_trade(user_id)

async def process_trade_with_dm(ctx, code, dm_message, trades_amount):
    """Processa um trade em segundo plano e envia atualizações via DM"""
    # Obter informações do código
    code_info = active_trades[code]
    expire_minutes = code_info.get('expire_minutes', 60)
    
    # Atualizar status
    code_info['status'] = 'processing'
    
    # Atualizar no MongoDB
    if db.is_connected():
        db.update_active_trade_status(code, 'processing')
    
    await dm_message.edit(content=f"⌛ Processando {trades_amount} trade(s) com código: **{code}**... Isso pode levar alguns segundos.")
    
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
                    title="✅ Trade Configurado com Sucesso!",
                    description=f"Seu código de trade foi processado para {trades_amount} trade(s).",
                    color=0x00ff00
                )
                embed.add_field(name="Código", value=f"**{code}**", inline=False)
                
                embed.add_field(
                    name="Seu trade foi finalizado com sucesso.", 
                    value="Para ganhar mais trades, participe das atividades e eventos dentro do servidor.", 
                    inline=False
                )
                embed.add_field(
                    name="Criado por:", 
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
                    title="✅ Trade Configurado com Sucesso!",
                    description=f"{ctx.author.mention} Você finalizou todos seus trades com sucesso.",
                    color=0x00ff00
                )
                public_embed.add_field(
                    name="Detalhes", 
                    value="Os detalhes foram enviados por mensagem privada.", 
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
                    title="❌ Falha ao processar trade",
                    description=f"Ocorreu um erro ao processar o código **{code}**.",
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
                await ctx.send(f"❌ {ctx.author.mention} Ocorreu um erro ao processar seu trade. Verifique sua mensagem privada para mais detalhes.")
                
        except Exception as e:
            code_info['status'] = 'failed'
            
            # Atualizar no MongoDB
            if db.is_connected():
                db.update_active_trade_status(code, 'failed')
            
            # Send error via DM
            await dm_message.edit(content=f"❌ Erro ao processar trade: {str(e)}")
            
            # Also notify about the error in public
            await ctx.send(f"❌ {ctx.author.mention} Ocorreu um erro ao processar seu trade. Verifique sua mensagem privada para mais detalhes.")

# Update your process_trade variable to use the new DM function
process_trade = process_trade_with_dm   # You can keep this for admin commands
            
            
@bot.command(name='ajuda')
async def help_command(ctx):
    """Exibe ajuda sobre os comandos do bot"""
    if ctx.author.guild_permissions.administrator:
        # Se for admin, mostra também a ajuda de admin
        await adminhelp_command(ctx)
    
    embed = discord.Embed(
        title="📚 Ajuda do Bot de Trades",
        description="Aqui estão os comandos disponíveis para todos os usuários:",
        color=0xffbb00
    )
    
    embed.add_field(
        name="!listtrades", 
        value="Mostra quantos trades você tem disponíveis.", 
        inline=False
    )
    
    embed.add_field(
        name="!claimtrade", 
        value="Recebe seus 5 trades diários (disponível a cada 24 horas).", 
        inline=False
    )
    
    embed.add_field(
        name="!usetrade [quantidade]", 
        value="Usa um dos seus trades disponíveis e gera um código para processar a quantidade especificada de trades.\n" +
              "Exemplo: `!usetrade 2` - Usa um trade para processar 2 trades.\n" +
              "⚠️ Você só pode ter um trade ativo por vez. Aguarde o processamento para usar outro.",
        inline=False
    )
    
    embed.add_field(
        name="!ajuda", 
        value="Exibe esta mensagem de ajuda", 
        inline=False
    )
    
    await ctx.send(embed=embed)

@bot.command(name='adminhelp')
@commands.has_permissions(administrator=True)  # Restringe apenas para administradores
async def adminhelp_command(ctx):
    """Exibe ajuda sobre os comandos de administrador"""
    embed = discord.Embed(
        title="🔒 Comandos de Administrador",
        description="Comandos disponíveis apenas para administradores:",
        color=0xff5500
    )
    
    embed.add_field(
        name="!trade [quantidade] [tempo_expiração]", 
        value="Gera novos códigos de trade e inicia o processamento automaticamente.\n" +
              "Exemplo: `!trade 3 60` - Gera 3 trades que expiram em 60 minutos.", 
        inline=False
    )
    
    embed.add_field(
        name="!timemode [duração] [tempo_expiração]", 
        value="Inicia o processamento contínuo de trades por um período específico.\n" +
              "Exemplo: `!timemode 20 60` - Processa trades por 20 minutos com um código que expira em 60 minutos.", 
        inline=False
    )
    
    embed.add_field(
        name="!status [código]", 
        value="Verifica o status de um trade específico. Se não for fornecido um código, mostra todos os seus trades ativos.", 
        inline=False
    )
    
    embed.add_field(
        name="!givetrade [@usuário] [quantidade]", 
        value="Dá uma quantidade específica de trades para um usuário.\n" +
              "Exemplo: `!givetrade @João 10` - Dá 10 trades para o usuário João.", 
        inline=False
    )
    
    await ctx.send(embed=embed)

@bot.command(name='helpdb')
@commands.has_permissions(administrator=True)  # Restringe apenas para administradores
async def helpdb_command(ctx):
    """Exibe informações sobre o status da conexão com o banco de dados"""
    embed = discord.Embed(
        title="🗄️ Status do Banco de Dados",
        color=0x0088ff
    )
    
    if db.is_connected():
        embed.description = "✅ Conexão com MongoDB estabelecida com sucesso!"
        embed.add_field(
            name="Informações", 
            value="Os dados de trades e cooldowns de usuários estão sendo persistidos no MongoDB.", 
            inline=False
        )
        
        # Adicionar estatísticas
        user_trades_count = len(user_trades)
        daily_cooldown_count = len(daily_claim_cooldown)
        active_trades_count = len(active_trades)
        active_users_count = len(users_with_active_trade)
        
        embed.add_field(
            name="Estatísticas", 
            value=f"- Usuários com trades: {user_trades_count}\n" +
                  f"- Usuários com cooldown: {daily_cooldown_count}\n" +
                  f"- Trades ativos: {active_trades_count}\n" +
                  f"- Usuários com trades em andamento: {active_users_count}",
            inline=False
        )
    else:
        embed.description = "⚠️ MongoDB não está conectado!"
        embed.add_field(
            name="Atenção", 
            value="O bot está operando com armazenamento em memória. Os dados serão perdidos quando o bot for reiniciado.", 
            inline=False
        )
        embed.add_field(
            name="Solução", 
            value="Configure a variável de ambiente `MONGO_URI` no arquivo `.env` para habilitar a persistência de dados.", 
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
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Este comando está disponível apenas para administradores.")

# Adicionar função de tratamento de erros para explicar quando comandos devem ser usados no canal correto
@listtrades_command.error
@claimtrade_command.error
@usetrade_command.error
async def channel_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        if TRADE_CHANNEL_ID:
            trade_channel = bot.get_channel(int(TRADE_CHANNEL_ID))
            if trade_channel:
                await ctx.send(f"❌ Este comando deve ser usado no canal {trade_channel.mention}.")
            else:
                await ctx.send("❌ Este comando deve ser usado no canal de trades designado.")
        else:
            await ctx.send("❌ Este comando não pode ser usado neste contexto.")

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
    
    bot.run(TOKEN)