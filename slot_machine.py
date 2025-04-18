import discord
from discord.ext import commands
import random
import asyncio
import datetime
from typing import Dict, List, Optional

# Importar a classe Database do seu sistema existente
from database import Database
from translations import t, get_user_language  # Importar funções de tradução

# ==============================================
# Configuração e Constantes
# ==============================================

# Símbolos do caça-níquel e suas recompensas
SLOT_SYMBOLS = [
    {"symbol": "🍀", "reward": 3, "rarity": "epic", "probability": 0.2},    # 20% chance, 3 trades, épico
    {"symbol": "⚽", "reward": 2, "rarity": "rare", "probability": 0.3},     # 30% chance, 2 trades, raro
    {"symbol": "❌", "reward": 0, "rarity": None, "probability": 0.5}        # 50% chance, 0 trades
]

# Tempo de cooldown em segundos (15 minutos)
COOLDOWN_TIME = 15 * 60

# Inicializar a conexão com o banco de dados
db = Database()

# ==============================================
# Funções Auxiliares
# ==============================================

def spin_slot_machine() -> List[str]:
    """Girar o caça-níquel e retornar o resultado"""
    results = []
    
    # Determinar os três símbolos com base na probabilidade
    for _ in range(3):
        rand = random.random()
        cumulative_probability = 0
        
        for item in SLOT_SYMBOLS:
            cumulative_probability += item["probability"]
            if rand < cumulative_probability:
                results.append(item["symbol"])
                break
    
    # Ocasionalmente forçar uma vitória para aumentar a diversão (15% de chance)
    should_force_win = random.random() < 0.15
    
    if should_force_win and not (results[0] == results[1] == results[2]):
        # Escolher um símbolo aleatório e fazer todas as posições iguais
        winning_symbol_index = random.randint(0, len(SLOT_SYMBOLS) - 1)
        winning_symbol = SLOT_SYMBOLS[winning_symbol_index]["symbol"]
        
        results = [winning_symbol, winning_symbol, winning_symbol]
    
    return results

async def give_reward(user_id: int, reward_count: int, rarity: str) -> bool:
    """Dar a recompensa ao usuário"""
    try:
        # Atualizar a contagem de trades do usuário no seu banco de dados
        if db.is_connected():
            db.increment_user_trades(user_id, reward_count)
            print(f"✅ {reward_count} trades adicionados para o usuário {user_id} (raridade: {rarity})")
        return True
    except Exception as e:
        print(f"❌ Erro ao dar recompensa: {e}")
        return False

async def is_on_cooldown(user_id: int) -> tuple:
    """Verificar se o usuário está em cooldown e retornar o tempo restante em segundos"""
    if db.is_connected():
        last_slot_time = db.get_slot_cooldown(user_id)
        
        if last_slot_time:
            now = datetime.datetime.now()
            time_diff = now - last_slot_time
            
            if time_diff.total_seconds() < COOLDOWN_TIME:
                seconds_left = COOLDOWN_TIME - time_diff.total_seconds()
                return True, int(seconds_left)
    
    return False, 0

async def set_cooldown(user_id: int):
    """Definir o cooldown para o usuário"""
    if db.is_connected():
        db.set_slot_cooldown(user_id, datetime.datetime.now())

# ==============================================
# Verificador para canal específico (opcional)
# ==============================================

def in_trade_channel():
    """Verificador para garantir que o comando seja usado apenas no canal de trades"""
    async def predicate(ctx):
        # Obter ID do canal de trades da configuração
        TRADE_CHANNEL_ID = ctx.bot.get_environment_var('TRADE_CHANNEL_ID', '')
        
        if not TRADE_CHANNEL_ID:
            return True  # Se não estiver configurado, permite em qualquer canal
        
        channel_id = str(ctx.channel.id)
        config_id = str(TRADE_CHANNEL_ID).strip()
        
        return channel_id == config_id
        
    return commands.check(predicate)

# ==============================================
# Comando de Caça-Níquel
# ==============================================

class SlotMachine(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='slot')
    @commands.guild_only()
    @in_trade_channel()  # Opcional - remova se quiser permitir em qualquer canal
    async def slot_command(self, ctx):
        """Jogar no caça-níquel e ganhar trades"""
        user_id = ctx.author.id
        lang = get_user_language(user_id)
        
        # Verificar cooldown
        on_cooldown, seconds_left = await is_on_cooldown(user_id)
        if on_cooldown:
            # Calcular minutos e segundos restantes
            minutes_left = seconds_left // 60
            remaining_seconds = seconds_left % 60
            
            time_str = ""
            if minutes_left > 0:
                time_str = f"{minutes_left}m {remaining_seconds}s"
            else:
                time_str = f"{remaining_seconds}s"
            
            # Criar embed com informações de cooldown
            cooldown_embed = discord.Embed(
                title=t('slot.title', lang),
                description=t('slot.onCooldown', lang, {'time': time_str}),
                color=0xFF5555
            )
            
            await ctx.send(embed=cooldown_embed)
            return
        
        # Criar embed inicial
        embed = discord.Embed(
            title=t('slot.title', lang),
            description=t('slot.description', lang),
            color=0x9933FF
        )
        embed.add_field(
            name=t('slot.rewards', lang),
            value=t('slot.rewardsDescription', lang),
            inline=False
        )
        embed.set_footer(text=t('slot.goodLuck', lang))
        
        # Enviar mensagem inicial
        message = await ctx.send(embed=embed)
        
        # Simular o giro do caça-níquel
        await asyncio.sleep(1)
        
        # Atualizar mensagem para mostrar que está girando
        spinning_embed = discord.Embed(
            title=t('slot.spinning', lang),
            description=t('slot.spinningDescription', lang),
            color=0x9933FF
        )
        
        await message.edit(embed=spinning_embed)
        
        # Esperar um pouco para simular o giro
        await asyncio.sleep(2)
        
        # Obter os resultados
        results = spin_slot_machine()
        
        # Verificar o resultado
        is_win = results[0] == results[1] == results[2]
        reward = 0
        rarity = None
        
        if is_win:
            # Encontrar o símbolo na lista e obter a recompensa e raridade
            winning_symbol = next((s for s in SLOT_SYMBOLS if s["symbol"] == results[0]), None)
            if winning_symbol:
                reward = winning_symbol["reward"]
                rarity = winning_symbol["rarity"]
        
        # Criar embed com o resultado
        result_embed = discord.Embed(
            title=t('slot.result', lang),
            description=f"{results[0]} | {results[1]} | {results[2]}",
            timestamp=datetime.datetime.now()
        )
        
        # Adicionar informações com base no resultado
        if is_win and reward > 0:
            result_embed.color = 0x00FF00  # Verde
            
            # Obter texto da raridade para o embed
            rarity_text = t(f'slot.{rarity}Rarity', lang) if rarity else t('slot.commonRarity', lang)
            
            result_embed.add_field(
                name=t('slot.congratulations', lang),
                value=t('slot.winDescription', lang, {'count': reward, 'rarity': rarity_text}),
                inline=False
            )
            
            # Dar a recompensa
            await give_reward(user_id, reward, rarity)
            
        else:
            result_embed.color = 0xFF0000  # Vermelho
            result_embed.add_field(
                name=t('slot.tryAgain', lang),
                value=t('slot.loseDescription', lang),
                inline=False
            )
        
        result_embed.set_footer(text=t('slot.playAgain', lang))
        
        # Atualizar a mensagem com o resultado
        await message.edit(embed=result_embed)
        
        # Definir cooldown para o usuário
        await set_cooldown(user_id)
        
        # Enviar mensagem de recompensa se ganhou
        if is_win and reward > 0:
            rarity_text = t(f'slot.{rarity}Rarity', lang) if rarity else t('slot.commonRarity', lang)
            await ctx.send(
                content=t('slot.rewardReceived', lang, {'count': reward, 'rarity': rarity_text}),
                delete_after=10  # Apagar após 10 segundos
            )
    
    # Tratamento de erros para o comando slot
    @slot_command.error
    async def slot_command_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            # Erro de canal incorreto
            lang = get_user_language(ctx.author.id)
            
            # Obter o ID do canal de trades configurado
            TRADE_CHANNEL_ID = ctx.bot.get_environment_var('TRADE_CHANNEL_ID', '')
            
            if TRADE_CHANNEL_ID:
                trade_channel = self.bot.get_channel(int(TRADE_CHANNEL_ID))
                if trade_channel:
                    await ctx.send(t('wrong_channel', lang, {'channel': trade_channel.mention}))
                else:
                    await ctx.send(t('command_unavailable', lang))
            else:
                await ctx.send(t('command_unavailable', lang))
        else:
            # Outro tipo de erro
            lang = get_user_language(ctx.author.id)
            print(f"Erro no comando slot: {error}")
            await ctx.send(t('slot.error', lang))
            
    # ADICIONE O CÓDIGO DO COMANDO SLOTCLEAR AQUI
    @commands.command(name='slotclear')
    @commands.has_permissions(administrator=True)  # Restringe para administradores
    async def slotclear_command(self, ctx, member: discord.Member = None):
        """Comando para administradores limparem o cooldown de slot de um usuário"""
        # Obter idioma do usuário
        lang = get_user_language(ctx.author.id)
        
        # Se não for especificado um membro, mostrar a sintaxe correta
        if not member:
            await ctx.send(t('slot.clear_usage', lang) or "❌ Uso correto: `!slotclear @usuário`")
            return
        
        # Limpar o cooldown do usuário no banco de dados
        if db.is_connected():
            success = db.clear_command_cooldown(member.id, "slot")
            
            if success:
                # Feedback de sucesso
                await ctx.send(
                    t('slot.clear_success', lang, {'user': member.display_name}) or 
                    f"✅ Cooldown de slot removido para {member.display_name}!"
                )
                
                # Notificar o usuário via DM que pode jogar novamente
                try:
                    user_lang = get_user_language(member.id)
                    dm_message = t('slot.clear_dm', user_lang) or "🎰 Um administrador resetou seu tempo de espera para o minigame de slot! Você já pode jogar novamente usando o comando `!slot`."
                    await member.send(dm_message)
                    # Indicar que a DM foi enviada
                    await ctx.message.add_reaction('✉️')
                except:
                    # Se não conseguir enviar DM, apenas ignorar
                    pass
            else:
                # Mensagem de erro
                await ctx.send(
                    t('slot.clear_error', lang) or 
                    "❌ Erro ao limpar o cooldown. Verifique a conexão com o banco de dados."
                )
        else:
            await ctx.send(
                t('slot.db_not_connected', lang) or 
                "❌ Banco de dados não está conectado."
            )

    # Tratamento de erros para o comando slotclear
    @slotclear_command.error
    async def slotclear_command_error(self, ctx, error):
        lang = get_user_language(ctx.author.id)
        
        if isinstance(error, commands.MissingPermissions):
            # Erro de permissões insuficientes
            await ctx.send(
                t('slot.admin_only', lang) or 
                "❌ Este comando é apenas para administradores."
            )
        elif isinstance(error, commands.MemberNotFound):
            # Erro de membro não encontrado
            await ctx.send(
                t('slot.member_not_found', lang) or 
                "❌ Usuário não encontrado. Verifique se você mencionou corretamente."
            )
        else:
            # Outro tipo de erro
            print(f"Erro no comando slotclear: {error}")
            await ctx.send(
                t('slot.error', lang) or 
                "❌ Ocorreu um erro ao executar o comando."
            )
            
def setup(bot):
    bot.add_cog(SlotMachine(bot))
            
        
