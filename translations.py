# translations.py - Sistema de tradução para o bot Discord

# Dicionário com todas as traduções
TRANSLATIONS = {
    # Português (Brasil) - Idioma padrão
    'pt': {
        # Mensagens gerais
        'trade_code_generated': '🔄 Gerando código de trade... Código: **{code}** (expira em {minutes} minutos)',
        'trade_time_mode': '🔄 Iniciando modo tempo com código: **{code}** | Processando trades por {duration} minutos (expira em {minutes} min)',
        'trade_processing': '⌛ Processando {amount} trade(s) com código: **{code}**... Isso pode levar alguns segundos.',
        'trade_success': '✅ Trade Configurado com Sucesso!',
        'trade_success_desc': 'Seu código de trade foi processado para {amount} trade(s).',
        'trade_success_public': '{mention} Você finalizou todos seus trades com sucesso.',
        'trade_details_sent': 'Os detalhes foram enviados por mensagem privada.',
        'trade_error': '❌ Falha ao processar trade',
        'trade_error_desc': 'Ocorreu um erro ao processar o código **{code}**.',
        'trade_error_public': '❌ {mention} Ocorreu um erro ao processar seu trade. Verifique sua mensagem privada para mais detalhes.',
        'trade_by': 'Criado por: Math',
        'trade_completed': 'Seu trade foi finalizado com sucesso.',
        'trade_more_info': 'Para ganhar mais trades, participe das atividades e eventos dentro do servidor.',
        
        # DM Trade
        'trades_received_title': '🎁 Você recebeu Trades!',
        'trades_received_desc': 'Você recebeu {amount} trade(s) do administrador {admin}.',
        'current_trades': 'Trades Atuais',
        'dm_blocked': '⚠️ Não foi possível enviar mensagem privada para {user} - DMs bloqueadas.',
        'dm_error': '⚠️ Erro ao enviar mensagem privada para {user}.',
        'trades_added': '✅ {amount} trade(s) adicionado(s) para {user}. Total atual: {total} trades.',
        'trade_amount_invalid': '❌ Quantidade de trades inválida. Use entre 1 e 100.',
        'member_not_found': '❌ Membro não encontrado ou offline.',
        
        # Erros e avisos
        'invalid_trades_count': '⚠️ Você pode solicitar entre 1 e 10 trades.',
        'invalid_expiry_time': '⚠️ O tempo de expiração deve estar entre 1 e 120 minutos.',
        'max_active_trades': '⚠️ Você só pode ter até 3 trades ativos. Você já tem {count} trade(s).',
        'system_busy': '⚠️ O sistema está processando muitos trades no momento. Por favor, tente novamente em alguns minutos.',
        'invalid_duration': '⚠️ A duração do processamento deve estar entre 1 e 120 minutos.',
        'no_active_trades': '❌ Você não tem trades ativos no momento.',
        'code_not_found': '❌ Código não encontrado: {code}',
        'not_your_code': '❌ Este código não pertence a você.',
        'trade_amount_invalid': '⚠️ A quantidade de trades deve estar entre 1 e 100.',
        'no_trades_available': '❌ Você não possui trades disponíveis. Use `!claimtrade` para obter trades diários ou peça a um administrador.',
        'trade_already_active': '⚠️ Você já possui um trade ativo com o código **{code}**. Aguarde até que ele seja concluído antes de usar outro trade.',
        'not_enough_trades': '❌ Você não possui trades suficientes. Você tem {available} trade(s) disponível(is), mas solicitou {requested}.',
        'cooldown_active': '⏰ Você já recebeu seus trades diários. Aguarde **{hours} horas e {minutes} minutos** para receber novamente.',
        'admin_only': '❌ Este comando está disponível apenas para administradores.',
        'wrong_channel': '❌ Este comando deve ser usado no canal {channel}.',
        'command_unavailable': '❌ Este comando não pode ser usado neste contexto.',
        
        # Status de trades
        'status_pending': 'Aguardando processamento',
        'status_processing': 'Em processamento',
        'status_completed': '✅ Concluído com sucesso',
        'status_failed': '❌ Falha no processamento',
        'mode_time': 'Modo tempo',
        'mode_trades': 'Modo trades',
        
        # Comandos e respostas
        'trades_added': '✅ {amount} trade(s) adicionado(s) para {user}. Total atual: **{total}**',
        'trades_available': '🎮 Você possui **{count}** trade(s) disponível(is).',
        'trades_claimed': '🎁 Você recebeu **5 trades diários**! Agora você possui **{total}** trade(s).',
        'trades_used': 'ℹ️ Trade utilizado! Você ainda possui **{count}** trade(s) disponível(is).',
        'generating_trades': '🔄 Gerando um trade com {amount} trocas para {mention}... Detalhes enviados por mensagem privada.',
        
        # Títulos das embeds
        'embed_active_trades': '🔍 Seus Trades Ativos',
        'embed_active_trades_desc': 'Você tem {count} trade(s) ativo(s):',
        'embed_trade_status': '🔍 Status do Trade: {code}',
        'embed_help_title': '📚 Ajuda do Bot de Trades',
        'embed_help_desc': 'Aqui estão os comandos disponíveis para todos os usuários:',
        'embed_admin_help': '🔒 Comandos de Administrador',
        'embed_admin_help_desc': 'Comandos disponíveis apenas para administradores:',
        'embed_db_status': '🗄️ Status do Banco de Dados',
        
        # Comandos de ajuda
        'help_listtrades': 'Mostra quantos trades você tem disponíveis.',
        'help_claimtrade': 'Recebe seus 5 trades diários (disponível a cada 24 horas).',
        'help_usetrade': 'Usa um dos seus trades disponíveis e gera um código para processar a quantidade especificada de trades.\nExemplo: `!usetrade 2` - Usa um trade para processar 2 trades.\n⚠️ Você só pode ter um trade ativo por vez. Aguarde o processamento para usar outro.',
        'help_help': 'Exibe esta mensagem de ajuda',
        'help_lang': 'Define seu idioma preferido. Opções disponíveis: pt (Português), en (Inglês), es (Espanhol).',
        
        # MongoDB e outros
        'db_connected': '✅ Conexão com MongoDB estabelecida com sucesso!',
        'db_info': 'Os dados de trades e cooldowns de usuários estão sendo persistidos no MongoDB.',
        'db_disconnected': '⚠️ MongoDB não está conectado!',
        'db_memory_warning': 'O bot está operando com armazenamento em memória. Os dados serão perdidos quando o bot for reiniciado.',
        'db_solution': 'Configure a variável de ambiente `MONGO_URI` no arquivo `.env` para habilitar a persistência de dados.',
        'db_stats': '- Usuários com trades: {users}\n- Usuários com cooldown: {cooldowns}\n- Trades ativos: {active}\n- Usuários com trades em andamento: {in_progress}',

        # Comandos de idioma
        'current_language': 'Seu idioma atual é: **{language}**',
        'available_languages': 'Idiomas disponíveis: {languages}',
        'invalid_language': '⚠️ Código de idioma inválido: "{code}". Use pt, en ou es.',
        'language_updated': '✅ Seu idioma foi alterado para **{language}**!',
    },
    
    # Inglês
    'en': {
        # Mensagens gerais
        'trade_code_generated': '🔄 Generating trade code... Code: **{code}** (expires in {minutes} minutes)',
        'trade_time_mode': '🔄 Starting time mode with code: **{code}** | Processing trades for {duration} minutes (expires in {minutes} min)',
        'trade_processing': '⌛ Processing {amount} trade(s) with code: **{code}**... This may take a few seconds.',
        'trade_success': '✅ Trade Successfully Configured!',
        'trade_success_desc': 'Your trade code has been processed for {amount} trade(s).',
        'trade_success_public': '{mention} You have successfully completed all your trades.',
        'trade_details_sent': 'Details have been sent via private message.',
        'trade_error': '❌ Failed to process trade',
        'trade_error_desc': 'An error occurred while processing the code **{code}**.',
        'trade_error_public': '❌ {mention} An error occurred while processing your trade. Check your private message for more details.',
        'trade_by': 'Created by: Math',
        'trade_completed': 'Your trade has been successfully completed.',
        'trade_more_info': 'To earn more trades, participate in activities and events within the server.',
        
        # DM Trade
        'trades_received_title': '🎁 You Received Trades!',
        'trades_received_desc': 'You received {amount} trade(s) from administrator {admin}.',
        'current_trades': 'Current Trades',
        'dm_blocked': '⚠️ Could not send private message to {user} - DMs blocked.',
        'dm_error': '⚠️ Error sending private message to {user}.',
        'trades_added': '✅ Added {amount} trade(s) for {user}. Current total: {total} trades.',
        'trade_amount_invalid': '❌ Invalid trade amount. Use between 1 and 100.',
        'member_not_found': '❌ Member not found or offline.',
            
        # Erros e avisos
        'invalid_trades_count': '⚠️ You can request between 1 and 10 trades.',
        'invalid_expiry_time': '⚠️ The expiration time must be between 1 and 120 minutes.',
        'max_active_trades': '⚠️ You can only have up to 3 active trades. You already have {count} trade(s).',
        'system_busy': '⚠️ The system is processing too many trades right now. Please try again in a few minutes.',
        'invalid_duration': '⚠️ The processing duration must be between 1 and 120 minutes.',
        'no_active_trades': '❌ You have no active trades at the moment.',
        'code_not_found': '❌ Code not found: {code}',
        'not_your_code': '❌ This code does not belong to you.',
        'trade_amount_invalid': '⚠️ The number of trades must be between 1 and 100.',
        'no_trades_available': '❌ You have no available trades. Use `!claimtrade` to get daily trades or ask an administrator.',
        'trade_already_active': '⚠️ You already have an active trade with the code **{code}**. Wait until it is completed before using another trade.',
        'not_enough_trades': '❌ You do not have enough trades. You have {available} trade(s) available, but requested {requested}.',
        'cooldown_active': '⏰ You have already received your daily trades. Wait **{hours} hours and {minutes} minutes** to receive again.',
        'admin_only': '❌ This command is only available to administrators.',
        'wrong_channel': '❌ This command must be used in the {channel} channel.',
        'command_unavailable': '❌ This command cannot be used in this context.',
        
        # Status de trades
        'status_pending': 'Waiting for processing',
        'status_processing': 'Processing',
        'status_completed': '✅ Successfully completed',
        'status_failed': '❌ Processing failed',
        'mode_time': 'Time mode',
        'mode_trades': 'Trades mode',
        
        # Comandos e respostas
        'trades_added': '✅ {amount} trade(s) added to {user}. Current total: **{total}**',
        'trades_available': '🎮 You have **{count}** trade(s) available.',
        'trades_claimed': '🎁 You received **5 daily trades**! Now you have **{total}** trade(s).',
        'trades_used': 'ℹ️ Trade used! You still have **{count}** trade(s) available.',
        'generating_trades': '🔄 Generating a trade with {amount} exchanges for {mention}... Details sent by private message.',
        
        # Títulos das embeds
        'embed_active_trades': '🔍 Your Active Trades',
        'embed_active_trades_desc': 'You have {count} active trade(s):',
        'embed_trade_status': '🔍 Trade Status: {code}',
        'embed_help_title': '📚 Trade Bot Help',
        'embed_help_desc': 'Here are the commands available to all users:',
        'embed_admin_help': '🔒 Administrator Commands',
        'embed_admin_help_desc': 'Commands available only to administrators:',
        'embed_db_status': '🗄️ Database Status',
        
        # Comandos de ajuda
        'help_listtrades': 'Shows how many trades you have available.',
        'help_claimtrade': 'Receive your 5 daily trades (available every 24 hours).',
        'help_usetrade': 'Uses one of your available trades and generates a code to process the specified number of trades.\nExample: `!usetrade 2` - Uses one trade to process 2 trades.\n⚠️ You can only have one active trade at a time. Wait for processing to use another.',
        'help_help': 'Displays this help message',
        'help_lang': 'Sets your preferred language. Available options: pt (Portuguese), en (English), es (Spanish).',
        
        # MongoDB e outros
        'db_connected': '✅ MongoDB connection established successfully!',
        'db_info': 'User trade data and cooldowns are being persisted in MongoDB.',
        'db_disconnected': '⚠️ MongoDB is not connected!',
        'db_memory_warning': 'The bot is operating with in-memory storage. Data will be lost when the bot is restarted.',
        'db_solution': 'Configure the `MONGO_URI` environment variable in the `.env` file to enable data persistence.',
        'db_stats': '- Users with trades: {users}\n- Users with cooldown: {cooldowns}\n- Active trades: {active}\n- Users with in-progress trades: {in_progress}',

        # Comandos de idioma
        'current_language': 'Your current language is: **{language}**',
        'available_languages': 'Available languages: {languages}',
        'invalid_language': '⚠️ Invalid language code: "{code}". Use pt, en or es.',
        'language_updated': '✅ Your language has been changed to **{language}**!',
    },
    
    # Espanhol
    'es': {
        # Mensagens gerais
        'trade_code_generated': '🔄 Generando código de intercambio... Código: **{code}** (expira en {minutes} minutos)',
        'trade_time_mode': '🔄 Iniciando modo tiempo con código: **{code}** | Procesando intercambios por {duration} minutos (expira en {minutes} min)',
        'trade_processing': '⌛ Procesando {amount} intercambio(s) con código: **{code}**... Esto puede tomar unos segundos.',
        'trade_success': '✅ ¡Intercambio Configurado con Éxito!',
        'trade_success_desc': 'Tu código de intercambio ha sido procesado para {amount} intercambio(s).',
        'trade_success_public': '{mention} Has finalizado todos tus intercambios con éxito.',
        'trade_details_sent': 'Los detalles han sido enviados por mensaje privado.',
        'trade_error': '❌ Error al procesar intercambio',
        'trade_error_desc': 'Ocurrió un error al procesar el código **{code}**.',
        'trade_error_public': '❌ {mention} Ocurrió un error al procesar tu intercambio. Revisa tu mensaje privado para más detalles.',
        'trade_by': 'Creado por: Math',
        'trade_completed': 'Tu intercambio ha sido finalizado con éxito.',
        'trade_more_info': 'Para ganar más intercambios, participa en las actividades y eventos dentro del servidor.',
        
        # DM Trade
        'trades_received_title': '🎁 ¡Recibiste Trades!',
        'trades_received_desc': 'Recibiste {amount} trade(s) del administrador {admin}.',
        'current_trades': 'Trades Actuales',
        'dm_blocked': '⚠️ No se pudo enviar mensaje privado a {user} - DMs bloqueados.',
        'dm_error': '⚠️ Error al enviar mensaje privado a {user}.',
        'trades_added': '✅ Añadidos {amount} trade(s) para {user}. Total actual: {total} trades.',
        'trade_amount_invalid': '❌ Cantidad de trades inválida. Use entre 1 y 100.',
        'member_not_found': '❌ Miembro no encontrado o desconectado.',
    
        # Erros e avisos
        'invalid_trades_count': '⚠️ Puedes solicitar entre 1 y 10 intercambios.',
        'invalid_expiry_time': '⚠️ El tiempo de expiración debe estar entre 1 y 120 minutos.',
        'max_active_trades': '⚠️ Solo puedes tener hasta 3 intercambios activos. Ya tienes {count} intercambio(s).',
        'system_busy': '⚠️ El sistema está procesando muchos intercambios en este momento. Por favor, inténtalo de nuevo en unos minutos.',
        'invalid_duration': '⚠️ La duración del procesamiento debe estar entre 1 y 120 minutos.',
        'no_active_trades': '❌ No tienes intercambios activos en este momento.',
        'code_not_found': '❌ Código no encontrado: {code}',
        'not_your_code': '❌ Este código no te pertenece.',
        'trade_amount_invalid': '⚠️ La cantidad de intercambios debe estar entre 1 y 100.',
        'no_trades_available': '❌ No tienes intercambios disponibles. Usa `!claimtrade` para obtener intercambios diarios o pide a un administrador.',
        'trade_already_active': '⚠️ Ya tienes un intercambio activo con el código **{code}**. Espera hasta que se complete antes de usar otro intercambio.',
        'not_enough_trades': '❌ No tienes suficientes intercambios. Tienes {available} intercambio(s) disponible(s), pero solicitaste {requested}.',
        'cooldown_active': '⏰ Ya has recibido tus intercambios diarios. Espera **{hours} horas y {minutes} minutos** para recibir nuevamente.',
        'admin_only': '❌ Este comando está disponible solo para administradores.',
        'wrong_channel': '❌ Este comando debe usarse en el canal {channel}.',
        'command_unavailable': '❌ Este comando no puede usarse en este contexto.',
        
        # Status de trades
        'status_pending': 'Esperando procesamiento',
        'status_processing': 'En procesamiento',
        'status_completed': '✅ Completado con éxito',
        'status_failed': '❌ Fallo en el procesamiento',
        'mode_time': 'Modo tiempo',
        'mode_trades': 'Modo intercambios',
        
        # Comandos e respostas
        'trades_added': '✅ {amount} intercambio(s) añadido(s) para {user}. Total actual: **{total}**',
        'trades_available': '🎮 Tienes **{count}** intercambio(s) disponible(s).',
        'trades_claimed': '🎁 ¡Has recibido **5 intercambios diarios**! Ahora tienes **{total}** intercambio(s).',
        'trades_used': 'ℹ️ ¡Intercambio utilizado! Aún tienes **{count}** intercambio(s) disponible(s).',
        'generating_trades': '🔄 Generando un intercambio con {amount} intercambios para {mention}... Detalles enviados por mensaje privado.',
        
        # Títulos das embeds
        'embed_active_trades': '🔍 Tus Intercambios Activos',
        'embed_active_trades_desc': 'Tienes {count} intercambio(s) activo(s):',
        'embed_trade_status': '🔍 Estado del Intercambio: {code}',
        'embed_help_title': '📚 Ayuda del Bot de Intercambios',
        'embed_help_desc': 'Aquí están los comandos disponibles para todos los usuarios:',
        'embed_admin_help': '🔒 Comandos de Administrador',
        'embed_admin_help_desc': 'Comandos disponibles solo para administradores:',
        'embed_db_status': '🗄️ Estado de la Base de Datos',
        
        # Comandos de ajuda
        'help_listtrades': 'Muestra cuántos intercambios tienes disponibles.',
        'help_claimtrade': 'Recibe tus 5 intercambios diarios (disponible cada 24 horas).',
        'help_usetrade': 'Usa uno de tus intercambios disponibles y genera un código para procesar la cantidad especificada de intercambios.\nEjemplo: `!usetrade 2` - Usa un intercambio para procesar 2 intercambios.\n⚠️ Solo puedes tener un intercambio activo a la vez. Espera a que se procese para usar otro.',
        'help_help': 'Muestra este mensaje de ayuda',
        'help_lang': 'Establece tu idioma preferido. Opciones disponibles: pt (Portugués), en (Inglés), es (Español).',
        
        # MongoDB e outros
        'db_connected': '✅ ¡Conexión con MongoDB establecida con éxito!',
        'db_info': 'Los datos de intercambios y tiempos de espera de los usuarios se están persistiendo en MongoDB.',
        'db_disconnected': '⚠️ ¡MongoDB no está conectado!',
        'db_memory_warning': 'El bot está operando con almacenamiento en memoria. Los datos se perderán cuando el bot se reinicie.',
        'db_solution': 'Configura la variable de entorno `MONGO_URI` en el archivo `.env` para habilitar la persistencia de datos.',
        'db_stats': '- Usuarios con intercambios: {users}\n- Usuarios con tiempo de espera: {cooldowns}\n- Intercambios activos: {active}\n- Usuarios con intercambios en progreso: {in_progress}',

        # Comandos de idioma
        'current_language': 'Tu idioma actual es: **{language}**',
        'available_languages': 'Idiomas disponibles: {languages}',
        'invalid_language': '⚠️ Código de idioma inválido: "{code}". Usa pt, en o es.',
        'language_updated': '✅ ¡Tu idioma ha sido cambiado a **{language}**!',
    }
}

# Função para traduzir uma mensagem
def translate(key, lang='pt', params=None):
    """
    Traduz uma chave para o idioma especificado
    
    Args:
        key (str): A chave de tradução
        lang (str): O código do idioma (pt, en, es)
        params (dict): Parâmetros para substituir no texto
        
    Returns:
        str: O texto traduzido
    """
    if params is None:
        params = {}
        
    # Se o idioma não existir, usa português como padrão
    if lang not in TRANSLATIONS:
        lang = 'pt'
        
    # Se a chave não existir no idioma, tenta em português
    text = TRANSLATIONS[lang].get(key)
    if text is None and lang != 'pt':
        text = TRANSLATIONS['pt'].get(key)
        
    # Se ainda não encontrou, retorna a chave
    if text is None:
        return key
        
    # Substitui parâmetros no texto
    for param, value in params.items():
        text = text.replace('{' + param + '}', str(value))
        
    return text

# Função de atalho para translate (para manter compatibilidade com o código existente)
def t(key, lang=None, params=None):
    """
    Função de atalho para translator.translate
    
    Args:
        key (str): A chave de tradução
        lang (str): O código do idioma (pt, en, es)
        params (dict): Parâmetros para substituir no texto
        
    Returns:
        str: O texto traduzido
    """
    from os import getenv
    
    # Se não foi especificado um idioma, usar o padrão do sistema
    if lang is None:
        lang = getenv('DEFAULT_LANGUAGE', 'pt')
    
    return translate(key, lang, params)

# Função para definir o idioma padrão
def set_lang(lang):
    """
    Função para definir o idioma padrão do sistema
    
    Args:
        lang (str): O código do idioma (pt, en, es)
    """
    import os
    
    if lang in TRANSLATIONS:
        os.environ['DEFAULT_LANGUAGE'] = lang
        print(f"🌐 Idioma padrão alterado para: {lang}")
    else:
        print(f"⚠️ Idioma '{lang}' não suportado. Idiomas disponíveis: {', '.join(TRANSLATIONS.keys())}")

# Função para obter o idioma do usuário
def get_user_language(user_id, guild_id=None):
    """
    Obtém o idioma preferido de um usuário
    
    Args:
        user_id (int): ID do usuário no Discord
        guild_id (int): ID do servidor (opcional)
        
    Returns:
        str: Código do idioma (pt, en, es)
    """
    from os import getenv
    
    # Normalmente, esta função verificaria o banco de dados
    # Para simplificar no Railway, vamos apenas retornar o idioma padrão
    return getenv('DEFAULT_LANGUAGE', 'pt')

# Lista de idiomas disponíveis
AVAILABLE_LANGUAGES = list(TRANSLATIONS.keys())
