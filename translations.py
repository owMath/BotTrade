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
        'trade_by': 'Criado por:',
        'trade_completed': 'Seu trade foi finalizado com sucesso.',
        'trade_more_info': 'Para ganhar mais trades, participe das atividades e eventos dentro do servidor.',
        'abort_no_code': 'Por favor, forneça o código do trade que deseja cancelar.',
        'abort_success_title': 'Trade Cancelado',
        'abort_success_desc': 'O trade com código **{code}** foi cancelado com sucesso.',
        'no_active_codes': 'Não há códigos ativos no momento.',
        'active_codes_title': 'Códigos Ativos',
        'active_codes_desc': 'Existem **{count}** códigos ativos no sistema.',
        'time_remaining': 'Tempo restante',
        'minutes': 'minutos',
        'status': 'Status',
        'help_activecodes': 'Mostra todos os códigos de trades ativos no sistema.',
        'check_trade_no_member': 'Por favor, mencione um usuário para verificar.',
        'check_trade_title': 'Trades de {user}',
        'check_trade_count': 'Quantidade de trades disponíveis',
        'check_trade_active': 'Trade ativo',
        'check_trade_no_active': 'Nenhum trade ativo',
        'check_trade_last_claim': 'Último claim diário',
        'check_trade_cooldown': 'Em cooldown (Próximo claim em: {hours}h {minutes}m)',
        'check_trade_can_claim': 'Pode fazer claim novamente',
        'check_trade_never_claimed': 'Nunca fez claim',
        'check_trade_timestamp': 'Último claim: {time}',
        'help_checktrademember': 'Verifica quantos trades um usuário possui e mostra informações sobre seu último claim diário.',   
        
        'help_trade': '!trade = quantidade fixa de trades, cada código processa um número exato de trades.',
        'help_timemode': '!timemode = duração fixa de tempo, o código processa trades enquanto durar o tempo.',
        'help_status': '!status = verifica o status do trade.',
        'help_givetrade': '!givetrade = dar trade para alguém.',
        'help_abort': '!abort = cancelar um code.',

        'bet_vote_success': 'Voto registrado com sucesso!',
        'bet_already_voted': 'Você já votou nesta opção.',
        'bet_closed': 'A aposta não está aberta para votação.',
        'bet_need_options': 'A aposta precisa de pelo menos 2 opções.',
        'bet_usage': 'Use: !bet Título Opção1 Opção2 [Opção3 ...]',
        'bet_not_found': 'Aposta com ID {id} não encontrada.',
        'bet_locked': 'A aposta já está travada ou encerrada.',
        'bet_already_ended': 'A aposta já foi encerrada.',

        # Dice
        'dice_result_title': '🎲 Resultado do Dado',
        'dice_result_desc': '{user} rolou dois dados!',
        'dice_roll': 'Rolagem',
        'dice_prize': 'Prêmio',
        'dice_win_3': '🎉 Parabéns! Você tirou 12 e ganhou **2 trades**!',  # Era 3 trades
        'dice_win_2': 'Muito bom! Você tirou 11 e ganhou **2 trades**!',   # Era 10 ou 11, agora só 11
        'dice_win_1': 'Você tirou 10 ou 7 e ganhou **1 trade**!',          # Era 7-9, agora só 10 e 7
        'dice_no_win': 'Não foi dessa vez! Tente novamente na próxima jogada.',
        'dice_total_trades': 'Total de Trades',
        'dice_total_count': 'Agora você tem **{count}** trades.',
        'dice_cooldown_title': '⏳ Cooldown do Dado Ativo',
        'dice_cooldown_desc': 'Você precisa esperar mais **{minutes} minutos e {seconds} segundos** para jogar novamente.',
        'dice_reminder_button': 'Lembrar quando disponível',
        'dice_reminder_set': 'Você receberá um lembrete em {minutes} minutos quando puder jogar novamente.',
        'dice_reminder_message': '🎲 O minigame do dado está disponível novamente! Use !dice para jogar.',
        'dice_already_available': 'O minigame já está disponível! Use !dice para jogar.',

        # Box Game
        'box_game_title': '🎮 Jogo das Caixas',
        'box_game_desc': '{user}, escolha uma das caixas abaixo! **Duas delas contêm um trade, as outras estão vazias.**',
        'box_game_prize_title': '🎁 Prêmio',
        'box_game_prize_desc': 'Se você escolher uma das caixas certas, ganhará 1 trade!',
        'box_win_title': '🎉 Você acertou!',
        'box_win_desc': 'Parabéns! Você escolheu a caixa {box} e ganhou o prêmio!',
        'box_lose_title': '😢 Não foi dessa vez...',
        'box_lose_desc': 'A caixa {box} estava vazia. Mais sorte na próxima vez!',
        'box_prize': '🎁 Seu prêmio',
        'box_trade_won': 'Você ganhou 1 trade!',
        'box_total_trades': '💼 Total de trades',
        'box_total_count': 'Agora você tem {count} trades disponíveis.',
        'box_try_again': '🔄 Tente novamente',
        'box_cooldown_info': 'Você poderá jogar novamente em 5 minutos.',
        'box_cooldown_title': '⏳ Cooldown Ativo',
        'box_cooldown_desc': 'Você precisa esperar {minutes} minutos e {seconds} segundos para jogar novamente.',
        'box_reminder_button': 'Lembrar quando disponível',
        'box_reminder_set': 'Você receberá um lembrete em {minutes} minutos quando puder jogar novamente.',
        'box_reminder_message': '🎮 O jogo da caixa está disponível novamente! Use !box para jogar.',
        'box_already_available': 'O jogo já está disponível! Use !box para jogar.',
        'not_your_game': 'Este não é o seu jogo! Use !box para iniciar seu próprio jogo.',

        'resetbox_no_member': 'Por favor, mencione um usuário para resetar o cooldown do jogo da caixa.',
        'resetbox_success': 'O cooldown do jogo da caixa de {user} foi resetado com sucesso.',
        'resetbox_not_on_cooldown': '{user} não está em cooldown do jogo da caixa.',
        'help_box': 'Jogar o jogo das caixas para ganhar trades.',
        'help_resetbox': 'Reseta o cooldown de box de um usuário.',
        'help_stats': 'Mostra estatísticas de trades. Períodos: all, today, week, month.',
        'help_giveaway': 'Inicia um sorteio de trades com restrição de cargo. Exemplo: !giveaway 60 1 5 @VIP Prêmio VIP',
        'help_resetuser': 'Resetar código de trade ativo de um usuário',
        'help_deletegiveaway': 'Deleta um sorteio ativo usando o ID da mensagem.',
        'giveaway_not_found': '❌ Mensagem de sorteio não encontrada.',
        'giveaway_no_permission': '❌ Sem permissão para acessar a mensagem do sorteio.',
        'giveaway_invalid_message': '❌ A mensagem especificada não é um sorteio válido.',
        'giveaway_deleted': '✅ Sorteio deletado com sucesso!',

        'giveaway_new_title': '🎉 Novo Giveaway!',
        'giveaway_new_desc': 'Prêmio: {prize}\n\nGanhadores: {winners}\nDuração: {duration} minutos\n\nClique no botão abaixo para participar!\n{description}',
        'giveaway_footer_id': 'ID: {id}',
        'giveaway_no_permission': 'Você não tem permissão para criar giveaways!',
        'giveaway_only_channel': 'Este comando só pode ser usado no canal <#{channel_id}>',
        'giveaway_ended_title': '🎉 Giveaway Encerrado',
        'giveaway_ended_desc': 'Prêmio: {prize}\n\nGanhadores: {winners}\n\nCada ganhador recebeu {prize}!',
        'giveaway_ended_no_participants': 'Ninguém participou deste giveaway!',
        'giveaway_deleted': 'Giveaway deletado com sucesso!',
        'giveaway_not_found': 'Giveaway não encontrado!',
        'giveaway_force_success': 'Giveaway encerrado com sucesso!',
        'giveaway_button_join': 'Participar',
        'giveaway_already_joined': 'Você já está participando deste giveaway!',
        'giveaway_join_success': 'Você entrou no giveaway com sucesso! Boa sorte! 🎉',
        'giveaway_already_ended': 'Este giveaway já foi encerrado!',
        'giveaway_dm': '🎉 Parabéns! Você ganhou **{trades}** trades no sorteio do servidor {server}!',
        
         # Sistema de Slot
        'slot_cooldown_title': '🕒 Cooldown do Slot Ativo',
        'slot_cooldown_desc': 'Você precisa esperar mais **{minutes} minutos e {seconds} segundos** para jogar novamente.',
        'slot_reminder_button': 'Lembrar-me quando disponível',
        'not_your_button': 'Este botão não é para você!',
        'slot_already_available': 'O slot já está disponível para uso!',
        'slot_reminder_set': 'Pronto! Vou te avisar quando puder jogar novamente em aproximadamente {minutes} minuto(s).',
        'slot_reminder_message': '⏰ **Lembrete:** O slot já está disponível para jogar novamente! Use o comando `!slot` para tentar a sorte!',
        'slot_result_title': '🎰 Resultado do Slot',
        'slot_result_desc': '{user} girou a slot machine!',
        'slot_machine': 'Slot Machine',
        'slot_result': 'Resultado',
        'slot_jackpot': '🏆 JACKPOT! Todos os símbolos iguais! Você ganhou 2 trades!',  # Era 3 trades
        'slot_two_match': '🎉 Dois símbolos iguais! Você ganhou 1 trade!',              # Era 2 trades
        'slot_no_match': '😢 Nenhuma combinação. Tente novamente mais tarde!',
        'slot_prize': 'Prêmio',
        'slot_trades_won': 'Você ganhou **{count}** trades!',
        'slot_total_trades': 'Total de Trades',
        'slot_total_count': 'Agora você tem **{count}** trades.',
        'resetslot_no_member': '⚠️ Você precisa mencionar um membro para resetar o cooldown do slot.',
        'resetslot_success': '✅ Cooldown de slot resetado para **{user}**.',
        'resetslot_not_on_cooldown': '📭 **{user}** não está em cooldown de slot.',
        'help_slot': 'Joga na slot machine para ganhar trades (cooldown de 5 minutos).',
        'help_resetslot': 'Reseta o cooldown de slot de um usuário (admin).',
        
        # Comando abort
        'abort_no_code': 'Por favor, forneça o código do trade que deseja cancelar.',
        'abort_success_title': 'Trade Cancelado',
        'abort_success_desc': 'O trade com código **{code}** foi cancelado com sucesso.',
        'help_abort': 'Cancela um trade ativo usando seu código.',
        
        # Comando activecodes
        'no_active_codes': 'Não há códigos ativos no momento.',
        'active_codes_title': 'Códigos Ativos',
        'active_codes_desc': 'Existem **{count}** códigos ativos no sistema.',
        'time_remaining': 'Tempo restante',
        'minutes': 'minutos',
        'status': 'Status',
        'help_activecodes': 'Mostra todos os códigos de trades ativos no sistema.',
        
        # Comando tradeshistory
        'history_no_permission': 'Você não tem permissão para ver o histórico de outro usuário.',
        'history_no_completed_trades': '{user} ainda não completou nenhum trade.',
        'history_no_trades': '{user} não realizou nenhum trade ainda.',
        'history_title': 'Histórico de Trades de {user}',
        'history_desc': 'Total de trades completados: {total}',
        'history_footer': 'Mostrando os 5 trades mais recentes.',
        'trades_amount': 'Quantidade',
        'trade_success': 'Sucesso',
        'trade_failed': 'Falhou',
        'help_tradeshistory': 'Mostra seu histórico de trades ou de um usuário específico (admin).',
        
        # Comando resetclaim
        'resetclaim_no_member': 'Você precisa especificar um usuário.',
        'resetclaim_success': 'O cooldown de claim diário de {user} foi resetado com sucesso.',
        'resetclaim_not_on_cooldown': '{user} não está em cooldown de claim diário.',
        'help_resetclaim': 'Reseta o cooldown de claim diário de um usuário.',
        
        # Comando stats
        'stats_invalid_period': 'Período inválido. Use um dos seguintes: {periods}',
        'stats_db_required': 'Este comando requer conexão com o banco de dados.',
        'stats_title': 'Estatísticas de Trades - {period}',
        'stats_desc': 'Resumo da atividade de trades no sistema.',
        'stats_total': 'Total de Trades',
        'stats_success': 'Trades com Sucesso',
        'stats_failed': 'Trades Falhos',
        'stats_avg_time': 'Tempo Médio',
        'stats_most_active': 'Usuário Mais Ativo',
        'stats_today': 'Hoje',
        'stats_week': 'Esta Semana',
        'stats_month': 'Este Mês',
        'stats_all_time': 'Todo o Período',
        'seconds': 'segundos',
        'help_stats': 'Mostra estatísticas de trades. Períodos: all, today, week, month.',

        # DM Trade
        'trades_received_title': '🎁 Você recebeu Trades!',
        'trades_received_desc': 'Você recebeu {amount} trade(s) do administrador {admin}. Use seus trades no {channel}!',
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
        'help_abort': 'Cancela um trade ativo usando seu código.',
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
        'invalid_language': '⚠️ Código de idioma inválido: "{code}". Use pt, en, es, de, it, fr, pl',
        'language_updated': '✅ Seu idioma foi alterado para **{language}**!',
        'specify_trades_amount': '⚠️ Por favor, especifique a quantidade de trades que deseja usar.\nExemplo: `!usetrade 1`',
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
        'trade_by': 'Created by:',
        'trade_completed': 'Your trade has been successfully completed.',
        'trade_more_info': 'To earn more trades, participate in activities and events within the server.',
        'abort_no_code': 'Please provide the trade code you want to cancel.',
        'abort_success_title': 'Trade Canceled',
        'abort_success_desc': 'The trade with code **{code}** has been successfully canceled.',
        'no_active_codes': 'There are no active codes at the moment.',
        'active_codes_title': 'Active Codes',
        'active_codes_desc': 'There are **{count}** active codes in the system.',
        'time_remaining': 'Time remaining',
        'minutes': 'minutes',
        'status': 'Status',
        'help_activecodes': 'Shows all active trade codes in the system.',
        'check_trade_no_member': 'Please mention a user to check.',
        'check_trade_title': '{user}\'s Trades',
        'check_trade_count': 'Available trades amount',
        'check_trade_active': 'Active trade',
        'check_trade_no_active': 'No active trade',
        'check_trade_last_claim': 'Last daily claim',
        'check_trade_cooldown': 'On cooldown (Next claim in: {hours}h {minutes}m)',
        'check_trade_can_claim': 'Can claim again',
        'check_trade_never_claimed': 'Never claimed',
        'check_trade_timestamp': 'Last claim: {time}',
        'help_checktrademember': 'Checks how many trades a user has and shows information about their last daily claim.',
    
        'giveaway_new_title': '🎉 New Giveaway!',
        'giveaway_new_desc': 'Prize: {prize}\n\nWinners: {winners}\nDuration: {duration} minutes\n\nClick the button below to participate!\n{description}',
        'giveaway_footer_id': 'ID: {id}',
        'giveaway_no_permission': 'You do not have permission to create giveaways!',
        'giveaway_only_channel': 'This command can only be used in channel <#{channel_id}>',
        'giveaway_ended_title': '🎉 Giveaway Ended',
        'giveaway_ended_desc': 'Prize: {prize}\n\nWinners: {winners}\n\nEach winner received {prize}!',
        'giveaway_ended_no_participants': 'No one participated in this giveaway!',
        'giveaway_deleted': 'Giveaway successfully deleted!',
        'giveaway_not_found': 'Giveaway not found!',
        'giveaway_force_success': 'Giveaway successfully ended!',
        'giveaway_button_join': 'Join',
        'giveaway_already_joined': 'You are already participating in this giveaway!',
        'giveaway_join_success': 'You have successfully joined the giveaway! Good luck! 🎉',
        'giveaway_already_ended': 'This giveaway has already ended!',
        'giveaway_dm': '🎉 Congratulations! You won **{trades}** trades in the giveaway on {server}!',

        'bet_vote_success': 'Vote registered successfully!',
        'bet_already_voted': 'You have already voted for this option.',
        'bet_closed': 'The bet is not open for voting.',
        'bet_need_options': 'The bet needs at least 2 options.',
        'bet_usage': 'Usage: !bet Title Option1 Option2 [Option3 ...]',
        'bet_not_found': 'Bet with ID {id} not found.',
        'bet_locked': 'The bet is already locked or ended.',
        'bet_already_ended': 'The bet has already ended.',

        # Dice
        'dice_result_title': '🎲 Dice Result',
        'dice_result_desc': '{user} rolled two dice!',
        'dice_roll': 'Roll',
        'dice_prize': 'Prize',
        'dice_win_3': '🎉 Congratulations! You rolled 12 and won **2 trades**!',  # Era 3 trades
        'dice_win_2': 'Great! You rolled 11 and won **2 trades**!',               # Era 10 or 11, agora só 11
        'dice_win_1': 'You rolled 10 or 7 and won **1 trade**!',                  # Era 7-9, agora só 10 e 7
        'dice_no_win': 'Not this time! Try again next time.',
        'dice_total_trades': 'Total Trades',
        'dice_total_count': 'You now have **{count}** trades.',
        'dice_cooldown_title': '⏳ Dice Cooldown Active',
        'dice_cooldown_desc': 'You need to wait **{minutes} minutes and {seconds} seconds** to play again.',
        'dice_reminder_button': 'Remind me when available',
        'dice_reminder_set': 'You will receive a reminder in {minutes} minutes when you can play again.',
        'dice_reminder_message': '🎲 The dice minigame is available again! Use !dice to play.',
        'dice_already_available': 'The minigame is already available! Use !dice to play.',

        # Box Game
        'box_game_title': '🎮 Box Game',
        'box_game_desc': '{user}, choose one of the boxes below! **Two of them contain a trade, the others are empty.**',
        'box_game_prize_title': '🎁 Prize',
        'box_game_prize_desc': 'If you choose one of the correct boxes, you will win 1 trade!',
        'box_win_title': '🎉 You got it!',
        'box_win_desc': 'Congratulations! You chose box {box} and won the prize!',
        'box_lose_title': '😢 Not this time...',
        'box_lose_desc': 'Box {box} was empty. Better luck next time!',
        'box_prize': '🎁 Your prize',
        'box_trade_won': 'You won 1 trade!',
        'box_total_trades': '💼 Total trades',
        'box_total_count': 'You now have {count} trades available.',
        'box_try_again': '🔄 Try again',
        'box_cooldown_info': 'You can play again in 5 minutes.',
        'box_cooldown_title': '⏳ Cooldown Active',
        'box_cooldown_desc': 'You need to wait {minutes} minutes and {seconds} seconds to play again.',
        'box_reminder_button': 'Remind me when available',
        'box_reminder_set': 'You will receive a reminder in {minutes} minutes when you can play again.',
        'box_reminder_message': '🎮 The box game is available again! Use !box to play.',
        'box_already_available': 'The game is already available! Use !box to play.',
        'not_your_game': 'This is not your game! Use !box to start your own game.',
        'resetbox_no_member': 'Please mention a user to reset the box game cooldown.',
        'resetbox_success': '{user}\'s box game cooldown has been reset successfully.',
        'resetbox_not_on_cooldown': '{user} is not on box game cooldown.',
        'help_box': 'Play the box game to earn trades.',
        'help_resetbox': 'Resets a user\'s box game cooldown.',
        
        # Sistema de Slot (em inglês)
        'slot_cooldown_title': '🕒 Slot Cooldown Active',
        'slot_cooldown_desc': 'You need to wait **{minutes} minutes and {seconds} seconds** to play again.',
        'slot_reminder_button': 'Remind me when available',
        'not_your_button': 'This button is not for you!',
        'slot_already_available': 'The slot is already available to use!',
        'slot_reminder_set': 'Done! I will notify you when you can play again in approximately {minutes} minute(s).',
        'slot_reminder_message': '⏰ **Reminder:** The slot is now available to play again! Use the `!slot` command to try your luck!',
        'slot_result_title': '🎰 Slot Result',
        'slot_result_desc': '{user} spun the slot machine!',
        'slot_machine': 'Slot Machine',
        'slot_result': 'Result',
        'slot_jackpot': '🏆 JACKPOT! All symbols match! You won 2 trades!',  # Era 3 trades
        'slot_two_match': '🎉 Two symbols match! You won 1 trade!',          # Era 2 trades
        'slot_no_match': '😢 No matches. Try again later!',
        'slot_prize': 'Prize',
        'slot_trades_won': 'You won **{count}** trades!',
        'slot_total_trades': 'Total Trades',
        'slot_total_count': 'You now have **{count}** trades.',
        'resetslot_no_member': '⚠️ You need to mention a member to reset their slot cooldown.',
        'resetslot_success': '✅ Slot cooldown reset for **{user}**.',
        'resetslot_not_on_cooldown': '📭 **{user}** is not on slot cooldown.',
        'help_slot': 'Play the slot machine to win trades (5-minute cooldown).',
        'help_resetslot': 'Reset a user\'s slot cooldown (admin only).',
        
        # Comando abort
        'abort_no_code': 'Please provide the trade code you want to cancel.',
        'abort_success_title': 'Trade Canceled',
        'abort_success_desc': 'The trade with code **{code}** has been successfully canceled.',
        'help_abort': 'Cancels an active trade using its code.',
        
        # Comando activecodes
        'no_active_codes': 'There are no active codes at the moment.',
        'active_codes_title': 'Active Codes',
        'active_codes_desc': 'There are **{count}** active codes in the system.',
        'time_remaining': 'Time remaining',
        'minutes': 'minutes',
        'status': 'Status',
        'help_activecodes': 'Shows all active trade codes in the system.',
        
        # Comando tradeshistory
        'history_no_permission': 'You do not have permission to view another user\'s history.',
        'history_no_completed_trades': '{user} has not completed any trades yet.',
        'history_no_trades': '{user} has not made any trades yet.',
        'history_title': '{user}\'s Trade History',
        'history_desc': 'Total completed trades: {total}',
        'history_footer': 'Showing the 5 most recent trades.',
        'trades_amount': 'Amount',
        'trade_success': 'Success',
        'trade_failed': 'Failed',
        'help_tradeshistory': 'Shows your trade history or a specific user\'s history (admin).',
        
        # Comando resetclaim
        'resetclaim_no_member': 'You need to specify a user.',
        'resetclaim_success': '{user}\'s daily claim cooldown has been successfully reset.',
        'resetclaim_not_on_cooldown': '{user} is not on daily claim cooldown.',
        'help_resetclaim': 'Resets a user\'s daily claim cooldown.',
        
        # Comando stats
        'stats_invalid_period': 'Invalid period. Use one of the following: {periods}',
        'stats_db_required': 'This command requires a database connection.',
        'stats_title': 'Trade Statistics - {period}',
        'stats_desc': 'Summary of trading activity in the system.',
        'stats_total': 'Total Trades',
        'stats_success': 'Successful Trades',
        'stats_failed': 'Failed Trades',
        'stats_avg_time': 'Average Time',
        'stats_most_active': 'Most Active User',
        'stats_today': 'Today',
        'stats_week': 'This Week',
        'stats_month': 'This Month',
        'stats_all_time': 'All Time',
        'seconds': 'seconds',
        'help_stats': 'Shows trade statistics. Periods: all, today, week, month.',
        
        # DM Trade
        'trades_received_title': '🎁 You Received Trades!',
        'trades_received_desc': 'You received {amount} trade(s) from administrator {admin}. Use your trades in {channel}!',
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
        'help_abort': 'Cancels an active trade using its code.',
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
        'invalid_language': '⚠️ Invalid language code: "{code}". Use pt, en, es, de, it, fr, pl',
        'language_updated': '✅ Your language has been changed to **{language}**!',
        'specify_trades_amount': '⚠️ Please specify the number of trades you want to use.\nExample: `!usetrade 1`',
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
        'trade_by': 'Creado por:',
        'trade_completed': 'Tu intercambio ha sido finalizado con éxito.',
        'trade_more_info': 'Para ganar más intercambios, participa en las actividades y eventos dentro del servidor.',
        'abort_no_code': 'Por favor, proporcione el código del trade que desea cancelar.',
        'abort_success_title': 'Trade Cancelado',
        'abort_success_desc': 'El trade con código **{code}** ha sido cancelado con éxito.',
        'no_active_codes': 'No hay códigos activos en este momento.',
        'active_codes_title': 'Códigos Activos',
        'active_codes_desc': 'Hay **{count}** códigos activos en el sistema.',
        'time_remaining': 'Tiempo restante',
        'minutes': 'minutos',
        'status': 'Estado',
        'help_activecodes': 'Muestra todos los códigos de trades activos en el sistema.',
        'check_trade_no_member': 'Por favor, menciona a un usuario para verificar.',
        'check_trade_title': 'Trades de {user}',
        'check_trade_count': 'Cantidad de trades disponibles',
        'check_trade_active': 'Trade activo',
        'check_trade_no_active': 'Sin trade activo',
        'check_trade_last_claim': 'Último claim diario',
        'check_trade_cooldown': 'En enfriamiento (Próximo claim en: {hours}h {minutes}m)',
        'check_trade_can_claim': 'Puede reclamar nuevamente',
        'check_trade_never_claimed': 'Nunca reclamó',
        'check_trade_timestamp': 'Último claim: {time}',
        'help_checktrademember': 'Verifica cuántos trades tiene un usuario y muestra información sobre su último claim diario.',

        'giveaway_new_title': '🎉 ¡Nuevo Sorteo!',
        'giveaway_new_desc': 'Premio: {prize}\n\nGanadores: {winners}\nDuración: {duration} minutos\n\n¡Haz clic en el botón de abajo para participar!\n{description}',
        'giveaway_footer_id': 'ID: {id}',
        'giveaway_no_permission': '¡No tienes permiso para crear sorteos!',
        'giveaway_only_channel': 'Este comando solo se puede usar en el canal <#{channel_id}>',
        'giveaway_ended_title': '🎉 Sorteo Finalizado',
        'giveaway_ended_desc': 'Premio: {prize}\n\nGanadores: {winners}\n\n¡Cada ganador recibió {prize}!',
        'giveaway_ended_no_participants': '¡Nadie participó en este sorteo!',
        'giveaway_deleted': '¡Sorteo eliminado con éxito!',
        'giveaway_not_found': '¡Sorteo no encontrado!',
        'giveaway_force_success': '¡Sorteo finalizado con éxito!',
        'giveaway_button_join': 'Participar',
        'giveaway_already_joined': '¡Ya estás participando en este sorteo!',
        'giveaway_join_success': '¡Te has unido al sorteo con éxito! ¡Buena suerte! 🎉',
        'giveaway_already_ended': '¡Este sorteo ya ha finalizado!',
        'giveaway_dm': '🎉 ¡Felicidades! Ganaste **{trades}** trades en el sorteo del servidor {server}!',
        'bet_vote_success': '¡Voto registrado con éxito!',
        'bet_already_voted': 'Ya has votado por esta opción.',
        'bet_closed': 'La apuesta no está abierta para votar.',
        'bet_need_options': 'La apuesta necesita al menos 2 opciones.',
        'bet_usage': 'Uso: !bet Título Opción1 Opción2 [Opción3 ...]',
        'bet_not_found': 'Apuesta con ID {id} no encontrada.',
        'bet_locked': 'La apuesta ya está bloqueada o finalizada.',
        'bet_already_ended': 'La apuesta ya ha finalizado.',

        # Dice
        'dice_result_title': '🎲 Resultado del Dado',
        'dice_result_desc': '¡{user} lanzó dos dados!',
        'dice_roll': 'Lanzamiento',
        'dice_prize': 'Premio',
        'dice_win_3': '🎉 ¡Felicidades! Sacaste 12 y ganaste **2 trades**!',      # Era 3 trades
        'dice_win_2': '¡Muy bien! Sacaste 11 y ganaste **2 trades**!',            # Era 10 o 11, agora só 11
        'dice_win_1': 'Sacaste 10 o 7 y ganaste **1 trade**!',                    # Era 7-9, agora só 10 e 7
        'dice_no_win': '¡No fue esta vez! ¡Inténtalo de nuevo la próxima vez!',
        'dice_total_trades': 'Total de Trades',
        'dice_total_count': 'Ahora tienes **{count}** trades.',
        'dice_cooldown_title': '⏳ Cooldown del Dado Activo',
        'dice_cooldown_desc': 'Necesitas esperar **{minutes} minutos y {seconds} segundos** para jugar de nuevo.',
        'dice_reminder_button': 'Recordarme cuando esté disponible',
        'dice_reminder_set': 'Recibirás un recordatorio en {minutes} minutos cuando puedas jugar de nuevo.',
        'dice_reminder_message': '🎲 El minijuego de dados está disponible de nuevo! Usa !dice para jugar.',
        'dice_already_available': '¡El minijuego ya está disponible! Usa !dice para jugar.',

        # Box Game
        'box_game_title': '🎮 Juego de las Cajas',
        'box_game_desc': '{user}, ¡elige una de las cajas abajo! **Dos de ellas contienen un trade, las otras están vacías.**',
        'box_game_prize_title': '🎁 Premio',
        'box_game_prize_desc': '¡Si eliges una de las cajas correctas, ganarás 1 trade!',
        'box_win_title': '🎉 ¡Acertaste!',
        'box_win_desc': '¡Felicidades! Elegiste la caja {box} y ganaste el premio!',
        'box_lose_title': '😢 No fue esta vez...',
        'box_lose_desc': 'La caja {box} estaba vacía. ¡Más suerte la próxima vez!',
        'box_prize': '🎁 Tu premio',
        'box_trade_won': '¡Ganaste 1 trade!',
        'box_total_trades': '💼 Total de trades',
        'box_total_count': 'Ahora tienes {count} trades disponibles.',
        'box_try_again': '🔄 Intenta de nuevo',
        'box_cooldown_info': 'Podrás jugar de nuevo en 5 minutos.',
        'box_cooldown_title': '⏳ Cooldown Activo',
        'box_cooldown_desc': 'Debes esperar {minutes} minutos y {seconds} segundos para jugar de nuevo.',
        'box_reminder_button': 'Recordar cuando esté disponible',
        'box_reminder_set': 'Recibirás un recordatorio en {minutes} minutos cuando puedas jugar de nuevo.',
        'box_reminder_message': '🎮 ¡El juego de las cajas está disponible de nuevo! Usa !box para jugar.',
        'box_already_available': '¡El juego ya está disponible! Usa !box para jugar.',
        'not_your_game': '¡Este no es tu juego! Usa !box para iniciar tu propio juego.',
        'resetbox_no_member': 'Por favor, menciona a un usuario para reiniciar el enfriamiento del juego de cajas.',
        'resetbox_success': 'El enfriamiento del juego de cajas de {user} ha sido reiniciado con éxito.',
        'resetbox_not_on_cooldown': '{user} no está en enfriamiento del juego de cajas.',
        'help_box': 'Juega al juego de cajas para ganar trades.',
        'help_resetbox': 'Reinicia el enfriamiento del juego de cajas de un usuario.',
        
         # Sistema de Slot (em espanhol)
        'slot_cooldown_title': '🕒 Enfriamiento de Tragamonedas Activo',
        'slot_cooldown_desc': 'Necesitas esperar **{minutes} minutos y {seconds} segundos** para jugar nuevamente.',
        'slot_reminder_button': 'Recuérdame cuando esté disponible',
        'not_your_button': '¡Este botón no es para ti!',
        'slot_already_available': '¡La tragamonedas ya está disponible para usar!',
        'slot_reminder_set': '¡Listo! Te avisaré cuando puedas jugar nuevamente en aproximadamente {minutes} minuto(s).',
        'slot_reminder_message': '⏰ **Recordatorio:** ¡La tragamonedas ya está disponible para jugar nuevamente! ¡Usa el comando `!slot` para probar tu suerte!',
        'slot_result_title': '🎰 Resultado de la Tragamonedas',
        'slot_result_desc': '¡{user} giró la tragamonedas!',
        'slot_machine': 'Tragamonedas',
        'slot_result': 'Resultado',
        'slot_jackpot': '🏆 ¡JACKPOT! ¡Todos los símbolos coinciden! ¡Ganaste 2 trades!',  # Era 3 trades
        'slot_two_match': '🎉 ¡Dos símbolos coinciden! ¡Ganaste 1 trade!',                  # Era 2 trades
        'slot_no_match': '😢 Sin coincidencias. ¡Inténtalo de nuevo más tarde!',
        'slot_prize': 'Premio',
        'slot_trades_won': '¡Ganaste **{count}** trades!',
        'slot_total_trades': 'Total de Trades',
        'slot_total_count': 'Ahora tienes **{count}** trades.',
        'resetslot_no_member': '⚠️ Debes mencionar a un miembro para reiniciar su enfriamiento de tragamonedas.',
        'resetslot_success': '✅ Enfriamiento de tragamonedas reiniciado para **{user}**.',
        'resetslot_not_on_cooldown': '📭 **{user}** no está en enfriamiento de tragamonedas.',
        'help_slot': 'Juega a la tragamonedas para ganar trades (enfriamiento de 5 minutos).',
        'help_resetslot': 'Reinicia el enfriamiento de tragamonedas de un usuario (solo admin).',
        
        # Comando abort
        'abort_no_code': 'Por favor, proporcione el código del trade que desea cancelar.',
        'abort_success_title': 'Trade Cancelado',
        'abort_success_desc': 'El trade con código **{code}** ha sido cancelado con éxito.',
        'help_abort': 'Cancela un trade activo usando su código.',
        
        # Comando activecodes
        'no_active_codes': 'No hay códigos activos en este momento.',
        'active_codes_title': 'Códigos Activos',
        'active_codes_desc': 'Hay **{count}** códigos activos en el sistema.',
        'time_remaining': 'Tiempo restante',
        'minutes': 'minutos',
        'status': 'Estado',
        'help_activecodes': 'Muestra todos los códigos de trades activos en el sistema.',
        
        # Comando tradeshistory
        'history_no_permission': 'No tienes permiso para ver el historial de otro usuario.',
        'history_no_completed_trades': '{user} aún no ha completado ningún trade.',
        'history_no_trades': '{user} no ha realizado ningún trade todavía.',
        'history_title': 'Historial de Trades de {user}',
        'history_desc': 'Total de trades completados: {total}',
        'history_footer': 'Mostrando los 5 trades más recientes.',
        'trades_amount': 'Cantidad',
        'trade_success': 'Éxito',
        'trade_failed': 'Fallido',
        'help_tradeshistory': 'Muestra tu historial de trades o el de un usuario específico (admin).',
        
        # Comando resetclaim
        'resetclaim_no_member': 'Necesitas especificar un usuario.',
        'resetclaim_success': 'El tiempo de espera de claim diario de {user} ha sido restablecido con éxito.',
        'resetclaim_not_on_cooldown': '{user} no está en tiempo de espera de claim diario.',
        'help_resetclaim': 'Restablece el tiempo de espera de claim diario de un usuario.',
        
        # Comando stats
        'stats_invalid_period': 'Período inválido. Usa uno de los siguientes: {periods}',
        'stats_db_required': 'Este comando requiere conexión a la base de datos.',
        'stats_title': 'Estadísticas de Trades - {period}',
        'stats_desc': 'Resumen de la actividad de trades en el sistema.',
        'stats_total': 'Total de Trades',
        'stats_success': 'Trades Exitosos',
        'stats_failed': 'Trades Fallidos',
        'stats_avg_time': 'Tiempo Promedio',
        'stats_most_active': 'Usuario Más Activo',
        'stats_today': 'Hoy',
        'stats_week': 'Esta Semana',
        'stats_month': 'Este Mes',
        'stats_all_time': 'Todo el Tiempo',
        'seconds': 'segundos',
        'help_stats': 'Muestra estadísticas de trades. Períodos: all, today, week, month.',
        
        # DM Trade
        'trades_received_title': '🎁 ¡Recibiste Trades!',
        'trades_received_desc': 'Has recibido {amount} trade(s) del administrador {admin}. ¡Usa tus trades en {channel}!',
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
        
        # Comandos de ayuda
        'help_listtrades': 'Muestra cuántos intercambios tienes disponibles.',
        'help_claimtrade': 'Recibe tus 5 intercambios diarios (disponible cada 24 horas).',
        'help_usetrade': 'Usa uno de tus intercambios disponibles y genera un código para procesar la cantidad especificada de intercambios.\nEjemplo: `!usetrade 2` - Usa un intercambio para procesar 2 intercambios.\n⚠️ Solo puedes tener un intercambio activo a la vez. Espera a que se procese para usar otro.',
        'help_help': 'Muestra este mensaje de ayuda',
        'help_abort': 'Cancela un trade activo usando su código.',
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
        'invalid_language': '⚠️ Código de idioma inválido: "{code}". Usa pt, en, es, de, it, fr, pl',
        'language_updated': '✅ ¡Tu idioma ha sido cambiado a **{language}**!',
        'specify_trades_amount': '⚠️ Por favor, especifica la cantidad de intercambios que deseas usar.\nEjemplo: `!usetrade 1`',
    },
    
    # Francês
'fr': {
    # Messages générales
    'trade_code_generated': '🔄 Génération du code de trade... Code: **{code}** (expire dans {minutes} minutes)',
    'trade_time_mode': '🔄 Démarrage du mode temps avec le code: **{code}** | Traitement des trades pendant {duration} minutes (expire dans {minutes} min)',
    'trade_processing': '⌛ Traitement de {amount} trade(s) avec le code: **{code}**... Cela peut prendre quelques secondes.',
    'trade_success': '✅ Trade Configuré avec Succès!',
    'trade_success_desc': 'Votre code de trade a été traité pour {amount} trade(s).',
    'trade_success_public': '{mention} Vous avez terminé tous vos trades avec succès.',
    'trade_details_sent': 'Les détails ont été envoyés par message privé.',
    'trade_error': '❌ Échec du traitement du trade',
    'trade_error_desc': 'Une erreur s\'est produite lors du traitement du code **{code}**.',
    'trade_error_public': '❌ {mention} Une erreur s\'est produite lors du traitement de votre trade. Vérifiez votre message privé pour plus de détails.',
    'trade_by': 'Créé par:',
    'trade_completed': 'Votre trade a été terminé avec succès.',
    'trade_more_info': 'Pour gagner plus de trades, participez aux activités et événements du serveur.',
    'abort_no_code': 'Veuillez fournir le code du trade que vous souhaitez annuler.',
    'abort_success_title': 'Trade Annulé',
    'abort_success_desc': 'Le trade avec le code **{code}** a été annulé avec succès.',
    'no_active_codes': 'Il n\'y a pas de codes actifs pour le moment.',
    'active_codes_title': 'Codes Actifs',
    'active_codes_desc': 'Il y a **{count}** codes actifs dans le système.',
    'time_remaining': 'Temps restant',
    'minutes': 'minutes',
    'status': 'Statut',
    'help_activecodes': 'Affiche tous les codes de trades actifs dans le système.',
    'check_trade_no_member': 'Veuillez mentionner un utilisateur à vérifier.',
    'check_trade_title': 'Trades de {user}',
    'check_trade_count': 'Nombre de trades disponibles',
    'check_trade_active': 'Trade actif',
    'check_trade_no_active': 'Aucun trade actif',
    'check_trade_last_claim': 'Dernière réclamation quotidienne',
    'check_trade_cooldown': 'En cooldown (Prochaine réclamation dans: {hours}h {minutes}m)',
    'check_trade_can_claim': 'Peut faire une réclamation',
    'check_trade_never_claimed': 'N\'a jamais fait de réclamation',
    'check_trade_timestamp': 'Dernière réclamation: {time}',
    'help_checktrademember': 'Vérifie le nombre de trades d\'un utilisateur et affiche des informations sur sa dernière réclamation quotidienne.',

    'giveaway_new_title': '🎉 Nouveau Giveaway !',
    'giveaway_new_desc': 'Prix : {prize}\n\nGagnants : {winners}\nDurée : {duration} minutes\n\nCliquez sur le bouton ci-dessous pour participer !\n{description}',
    'giveaway_footer_id': 'ID : {id}',
    'giveaway_no_permission': 'Vous n\'avez pas la permission de créer des giveaways !',
    'giveaway_only_channel': 'Cette commande ne peut être utilisée que dans le canal <#{channel_id}>',
    'giveaway_ended_title': '🎉 Giveaway Terminé',
    'giveaway_ended_desc': 'Prix : {prize}\n\nGagnants : {winners}\n\nChaque gagnant a reçu {prize}!',
    'giveaway_ended_no_participants': 'Personne n\'a participé à ce giveaway !',
    'giveaway_deleted': 'Giveaway supprimé avec succès !',
    'giveaway_not_found': 'Giveaway non trouvé !',
    'giveaway_force_success': 'Giveaway terminé avec succès !',
    'giveaway_button_join': 'Participer',
    'giveaway_already_joined': 'Vous participez déjà à ce giveaway !',
    'giveaway_join_success': 'Vous avez rejoint le giveaway avec succès ! Bonne chance ! 🎉',
    'giveaway_already_ended': 'Ce giveaway est déjà terminé !',
    'giveaway_dm': '🎉 Félicitations ! Vous avez gagné **{trades}** trades lors du giveaway sur le serveur {server} !',
    # DM Trade
    'trades_received_title': '🎁 Vous avez reçu des Trades !',
    'trades_received_desc': 'Vous avez reçu {amount} trade(s) de l\'administrateur {admin}. Utilisez vos trades dans {channel} !',
    'current_trades': 'Trades actuels',
    'dm_blocked': '⚠️ Impossible d\'envoyer un message privé à {user} - DMs bloqués.',
    'dm_error': '⚠️ Erreur lors de l\'envoi du message privé à {user}.',
    'trades_added': '✅ Ajouté {amount} trade(s) pour {user}. Total actuel : {total} trades.',
    'trade_amount_invalid': '❌ Montant de trade invalide. Utilisez entre 1 et 100.',
    'member_not_found': '❌ Membre introuvable ou hors ligne.',

    # Dice
    'dice_result_title': '🎲 Résultat du Dé',
    'dice_result_desc': '{user} a lancé deux dés !',
    'dice_roll': 'Lancer',
    'dice_prize': 'Prix',
    'dice_win_3': '🎉 Félicitations ! Vous avez fait 12 et gagné **2 trades** !',  # Era 3 trades
    'dice_win_2': 'Bravo ! Vous avez fait 11 et gagné **2 trades** !',             # Era 10 ou 11, agora só 11
    'dice_win_1': 'Vous avez fait 10 ou 7 et gagné **1 trade** !',                 # Era 7-9, agora só 10 e 7
    'dice_no_win': 'Pas cette fois ! Réessayez la prochaine fois !',
    'dice_total_trades': 'Total de Trades',
    'dice_total_count': 'Vous avez maintenant **{count}** trades.',
    'dice_cooldown_title': '⏳ Cooldown du Dé Actif',
    'dice_cooldown_desc': 'Vous devez attendre encore **{minutes} minutes et {seconds} secondes** pour rejouer.',
    'dice_reminder_button': 'Me rappeler quand disponible',
    'dice_reminder_set': 'Vous recevrez un rappel dans {minutes} minutes quand vous pourrez rejouer.',
    'dice_reminder_message': '🎲 Le mini-jeu de dés est à nouveau disponible ! Utilisez !dice pour jouer.',
    'dice_already_available': 'Le mini-jeu est déjà disponible ! Utilisez !dice pour jouer.',

    # Box Game
    'box_game_title': '🎮 Jeu des Boîtes',
    'box_game_desc': '{user}, choisissez une des boîtes ci-dessous ! **Deux d\'entre elles contiennent un trade, les autres sont vides.**',
    'box_game_prize_title': '🎁 Prix',
    'box_game_prize_desc': 'Si vous choisissez une des bonnes boîtes, vous gagnerez 1 trade !',
    'box_win_title': '🎉 Bravo !',
    'box_win_desc': 'Félicitations ! Vous avez choisi la boîte {box} et gagné le prix !',
    'box_lose_title': '😢 Pas cette fois...',
    'box_lose_desc': 'La boîte {box} était vide. Bonne chance la prochaine fois !',
    'box_prize': '🎁 Votre prix',
    'box_trade_won': 'Vous avez gagné 1 trade !',
    'box_total_trades': '💼 Total de trades',
    'box_total_count': 'Vous avez maintenant {count} trades disponibles.',
    'box_try_again': '🔄 Réessayez',
    'box_cooldown_info': 'Vous pourrez rejouer dans 5 minutes.',
    'box_cooldown_title': '⏳ Cooldown Actif',
    'box_cooldown_desc': 'Vous devez attendre {minutes} minutes et {seconds} secondes pour rejouer.',
    'box_reminder_button': 'Me rappeler quand disponible',
    'box_reminder_set': 'Vous recevrez un rappel dans {minutes} minutes lorsque vous pourrez rejouer.',
    'box_reminder_message': '🎮 Le jeu des boîtes est à nouveau disponible ! Utilisez !box pour jouer.',
    'box_already_available': 'Le jeu est déjà disponible ! Utilisez !box pour jouer.',
    'not_your_game': 'Ce n\'est pas votre jeu ! Utilisez !box pour démarrer votre propre jeu.',
    'resetbox_no_member': 'Veuillez mentionner un utilisateur pour réinitialiser le cooldown du jeu des boîtes.',
    'resetbox_success': 'Le cooldown du jeu des boîtes de {user} a été réinitialisé avec succès.',
    'resetbox_not_on_cooldown': '{user} n\'est pas en cooldown du jeu des boîtes.',
    'help_box': 'Jouer au jeu des boîtes pour gagner des trades.',
    'help_resetbox': 'Réinitialise le cooldown de box d\'un utilisateur.',

    # Système de Slot
    'slot_cooldown_title': '🕒 Cooldown du Slot Actif',
    'slot_cooldown_desc': 'Vous devez attendre encore **{minutes} minutes et {seconds} secondes** pour jouer à nouveau.',
    'slot_reminder_button': 'Me rappeler quand disponible',
    'not_your_button': 'Ce bouton n\'est pas pour vous!',
    'slot_already_available': 'Le slot est déjà disponible pour utilisation!',
    'slot_reminder_set': 'Prêt! Je vous préviendrai quand vous pourrez jouer à nouveau dans environ {minutes} minute(s).',
    'slot_reminder_message': '⏰ **Rappel:** Le slot est à nouveau disponible! Utilisez la commande `!slot`, pour tenter votre chance!',
    'slot_result_title': '🎰 Résultat du Slot',
    'slot_result_desc': '{user} a tourné la machine à sous!',
    'slot_machine': 'Machine à Sous',
    'slot_result': 'Résultat',
    'slot_jackpot': '🏆 JACKPOT ! Tous les symboles correspondent ! Vous avez gagné 2 trades !',  # Era 3 trades
    'slot_two_match': '🎉 Deux symboles correspondent ! Vous avez gagné 1 trade !',                # Era 2 trades
    'slot_no_match': '😢 Aucune combinaison. Réessayez plus tard!',
    'slot_prize': 'Prix',
    'slot_trades_won': 'Vous avez gagné **{count}** trades!',
    'slot_total_trades': 'Total des Trades',
    'slot_total_count': 'Vous avez maintenant **{count}** trades.',
    'resetslot_no_member': '⚠️ Vous devez mentionner un membre pour réinitialiser le cooldown du slot.',
    'resetslot_success': '✅ Cooldown de slot réinitialisé pour **{user}**.',
    'resetslot_not_on_cooldown': '📭 **{user}** n\'est pas en cooldown de slot.',
    'help_slot': 'Jouer à la machine à sous pour gagner des trades (cooldown de 5 minutes).',
    'help_resetslot': 'Réinitialise le cooldown de slot d\'un utilisateur (admin).',

    # Commandes et réponses
    'trades_added': '✅ {amount} trade(s) ajouté(s) pour {user}. Total actuel: **{total}**',
    'trades_available': '🎮 Vous avez **{count}** trade(s) disponible(s).',
    'trades_claimed': 'Vous avez reçu **5 trades quotidiens**! Vous avez maintenant **{total}** trade(s).',
    'trades_used': 'ℹ️ Trade utilisé! Vous avez encore **{count}** trade(s) disponible(s).',
    'generating_trades': '🔄 Génération d\'un trade avec {amount} échanges pour {mention}... Détails envoyés par message privé.',

    # Titres des embeds
    'embed_active_trades': '🔍 Vos Trades Actifs',
    'embed_active_trades_desc': 'Vous avez {count} trade(s) actif(s):',
    'embed_trade_status': '🔍 Statut du Trade: {code}',
    'embed_help_title': '📚 Aide du Bot de Trades',
    'embed_help_desc': 'Voici les commandes disponibles pour tous les utilisateurs:',
    'embed_admin_help': '🔒 Commandes d\'Administrateur',
    'embed_admin_help_desc': 'Commandes disponibles uniquement pour les administrateurs:',
    'embed_db_status': '🗄️ Statut de la Base de Données',

    # Commandes d'aide
    'help_listtrades': 'Affiche le nombre de trades que vous avez disponibles.',
    'help_claimtrade': 'Reçoit vos 5 trades quotidiens (disponible toutes les 24 heures).',
    'help_usetrade': 'Utilise un de vos trades disponibles et génère un code pour traiter la quantité spécifiée de trades.\nExemple: `!usetrade 2` - Utilise un trade pour traiter 2 trades.\n⚠️ Vous ne pouvez avoir qu\'un seul trade actif à la fois. Attendez le traitement pour en utiliser un autre.',
    'help_help': 'Affiche ce message d\'aide',
    'help_abort': 'Annule un trade actif en utilisant son code.',
    'help_lang': 'Définit votre langue préférée. Options disponibles: fr (Français), en (Anglais), es (Espagnol).',

    # Erreurs et avertissements
    'invalid_trades_count': '⚠️ Vous pouvez demander entre 1 et 10 trades.',
    'invalid_expiry_time': '⚠️ Le temps d\'expiration doit être entre 1 et 120 minutes.',
    'max_active_trades': '⚠️ Vous ne pouvez avoir que 3 trades actifs maximum. Vous avez déjà {count} trade(s).',
    'system_busy': '⚠️ Le système traite trop de trades en ce moment. Veuillez réessayer dans quelques minutes.',
    'invalid_duration': '⚠️ La durée de traitement doit être entre 1 et 120 minutes.',
    'no_active_trades': '❌ Vous n\'avez pas de trades actifs en ce moment.',
    'code_not_found': '❌ Code non trouvé: {code}',
    'not_your_code': '❌ Ce code ne vous appartient pas.',
    'trade_amount_invalid': '⚠️ Le nombre de trades doit être entre 1 et 100.',
    'no_trades_available': '❌ Vous n\'avez pas de trades disponibles. Utilisez `!claimtrade` pour obtenir des trades quotidiens ou demandez à un administrateur.',
    'trade_already_active': '⚠️ Vous avez déjà un trade actif avec le code **{code}**. Attendez qu\'il soit terminé avant d\'en utiliser un autre.',
    'not_enough_trades': '❌ Vous n\'avez pas assez de trades. Vous avez {available} trade(s) disponible(s), mais vous en avez demandé {requested}.',
    'cooldown_active': '⏰ Vous avez déjà reçu vos trades quotidiens. Attendez **{hours} heures et {minutes} minutes** pour en recevoir à nouveau.',
    'admin_only': '❌ Cette commande est réservée aux administrateurs.',
    'wrong_channel': '❌ Cette commande doit être utilisée dans le canal {channel}.',
    'command_unavailable': '❌ Cette commande n\'est pas disponible dans ce contexte.',

    # MongoDB et autres
    'db_connected': '✅ Connexion à MongoDB établie avec succès!',
    'db_info': 'Les données de trades et les cooldowns des utilisateurs sont persistés dans MongoDB.',
    'db_disconnected': '⚠️ MongoDB n\'est pas connecté!',
    'db_memory_warning': 'Le bot fonctionne avec un stockage en mémoire. Les données seront perdues lorsque le bot sera redémarré.',
    'db_solution': 'Configurez la variable d\'environnement `MONGO_URI` dans le fichier `.env` pour activer la persistance des données.',
    'db_stats': '- Utilisateurs avec trades: {users}\n- Utilisateurs en cooldown: {cooldowns}\n- Trades actifs: {active}\n- Utilisateurs avec trades en cours: {in_progress}',

    # Commandes de langue
    'current_language': 'Votre langue actuelle est: **{language}**',
    'available_languages': 'Langues disponibles: {languages}',
    'invalid_language': '⚠️ Code de langue invalide: "{code}". Utilisez pt, en, es, de, it, fr, pl',
    'language_updated': '✅ Votre langue a été changée pour **{language}**!',
    'specify_trades_amount': '⚠️ Veuillez spécifier le nombre de trades à utiliser.\nExemple : `!usetrade 1`',
    },

    # Alemão
'de': {
    # Allgemeine Nachrichten
    'trade_code_generated': '🔄 Trade-Code wird generiert... Code: **{code}** (läuft in {minutes} Minuten ab)',
    'trade_time_mode': '🔄 Zeitmodus wird gestartet mit Code: **{code}** | Verarbeitung von Trades für {duration} Minuten (läuft in {minutes} min ab)',
    'trade_processing': '⌛ Verarbeite {amount} Trade(s) mit Code: **{code}**... Dies kann einige Sekunden dauern.',
    'trade_success': '✅ Trade erfolgreich konfiguriert!',
    'trade_success_desc': 'Ihr Trade-Code wurde für {amount} Trade(s) verarbeitet.',
    'trade_success_public': '{mention} Sie haben alle Ihre Trades erfolgreich abgeschlossen.',
    'trade_details_sent': 'Die Details wurden per Privatnachricht gesendet.',
    'trade_error': '❌ Fehler bei der Verarbeitung des Trades',
    'trade_error_desc': 'Bei der Verarbeitung des Codes **{code}** ist ein Fehler aufgetreten.',
    'trade_error_public': '❌ {mention} Bei der Verarbeitung Ihres Trades ist ein Fehler aufgetreten. Bitte überprüfen Sie Ihre Privatnachrichten für weitere Details.',
    'trade_by': 'Erstellt von:',
    'trade_completed': 'Ihr Trade wurde erfolgreich abgeschlossen.',
    'trade_more_info': 'Um mehr Trades zu erhalten, nehmen Sie an Aktivitäten und Events im Server teil.',
    'abort_no_code': 'Bitte geben Sie den Code des Trades an, den Sie abbrechen möchten.',
    'abort_success_title': 'Trade abgebrochen',
    'abort_success_desc': 'Der Trade mit Code **{code}** wurde erfolgreich abgebrochen.',
    'no_active_codes': 'Es gibt derzeit keine aktiven Codes.',
    'active_codes_title': 'Aktive Codes',
    'active_codes_desc': 'Es gibt **{count}** aktive Codes im System.',
    'time_remaining': 'Verbleibende Zeit',
    'minutes': 'Minuten',
    'status': 'Status',
    'help_activecodes': 'Zeigt alle aktiven Trade-Codes im System an.',
    'check_trade_no_member': 'Bitte erwähnen Sie einen Benutzer zur Überprüfung.',
    'check_trade_title': 'Trades von {user}',
    'check_trade_count': 'Anzahl verfügbarer Trades',
    'check_trade_active': 'Aktiver Trade',
    'check_trade_no_active': 'Kein aktiver Trade',
    'check_trade_last_claim': 'Letzter täglicher Claim',
    'check_trade_cooldown': 'In Abklingzeit (Nächster Claim in: {hours}h {minutes}m)',
    'check_trade_can_claim': 'Kann wieder einen Claim machen',
    'check_trade_never_claimed': 'Hat noch nie einen Claim gemacht',
    'check_trade_timestamp': 'Letzter Claim: {time}',
    'help_checktrademember': 'Überprüft die Anzahl der Trades eines Benutzers und zeigt Informationen über seinen letzten täglichen Claim an.',

    'giveaway_new_title': '🎉 Neues Giveaway!',
    'giveaway_new_desc': 'Preis: {prize}\n\nGewinner: {winners}\nDauer: {duration} Minuten\n\nKlicke unten auf den Button, um teilzunehmen!\n{description}',
    'giveaway_footer_id': 'ID: {id}',
    'giveaway_no_permission': 'Du hast keine Berechtigung, Giveaways zu erstellen!',
    'giveaway_only_channel': 'Dieser Befehl kann nur im Kanal <#{channel_id}> verwendet werden',
    'giveaway_ended_title': '🎉 Giveaway Beendet',
    'giveaway_ended_desc': 'Preis: {prize}\n\nGewinner: {winners}\n\nJeder Gewinner hat {prize}!',
    'giveaway_ended_no_participants': 'Niemand hat an diesem Giveaway teilgenommen!',
    'giveaway_deleted': 'Giveaway erfolgreich gelöscht!',
    'giveaway_not_found': 'Giveaway nicht gefunden!',
    'giveaway_force_success': 'Giveaway erfolgreich beendet!',
    'giveaway_button_join': 'Teilnehmen',
    'giveaway_already_joined': 'Du nimmst bereits an diesem Giveaway teil!',
    'giveaway_join_success': 'Du hast erfolgreich am Giveaway teilgenommen! Viel Glück! 🎉',
    'giveaway_already_ended': 'Dieses Giveaway ist bereits beendet!',
    'giveaway_dm': '🎉 Glückwunsch! Du hast **{trades}** trades im Giveaway auf dem Server {server} gewonnen!',

    'bet_vote_success': 'Stimme erfolgreich registriert!',
    'bet_already_voted': 'Du hast bereits für diese Option abgestimmt.',
    'bet_closed': 'Die Wette ist nicht zur Abstimmung geöffnet.',
    'bet_need_options': 'Die Wette benötigt mindestens 2 Optionen.',
    'bet_usage': 'Verwendung: !bet Titel Option1 Option2 [Option3 ...]',
    'bet_not_found': 'Wette mit ID {id} nicht gefunden.',
    'bet_locked': 'Die Wette ist bereits gesperrt oder beendet.',
    'bet_already_ended': 'Die Wette wurde bereits beendet.',

    # DM Trade
    'trades_received_title': '🎁 Du hast Trades erhalten!',
    'trades_received_desc': 'Du hast {amount} Trade(s) vom Administrator {admin} erhalten. Verwende deine Trades in {channel}!',
    'current_trades': 'Aktuelle Trades',
    'dm_blocked': '⚠️ Konnte keine private Nachricht an {user} senden - DMs blockiert.',
    'dm_error': '⚠️ Fehler beim Senden der privaten Nachricht an {user}.',
    'trades_added': '✅ {amount} Trade(s) für {user} hinzugefügt. Aktueller Gesamtbetrag: {total} Trades.',
    'trade_amount_invalid': '❌ Ungültiger Trade-Betrag. Verwende zwischen 1 und 100.',
    'member_not_found': '❌ Mitglied nicht gefunden oder offline.',

    # Dice
    'dice_result_title': '🎲 Würfelergebnis',
    'dice_result_desc': '{user} hat zwei Würfel geworfen!',
    'dice_roll': 'Wurf',
    'dice_prize': 'Preis',
    'dice_win_3': '🎉 Glückwunsch! Du hast 12 geworfen und **2 Trades** gewonnen!',  # Era 3 trades
    'dice_win_2': 'Sehr gut! Du hast 11 geworfen und **2 Trades** gewonnen!',        # Era 10 oder 11, agora só 11
    'dice_win_1': 'Du hast 10 oder 7 geworfen und **1 Trade** gewonnen!',            # Era 7-9, agora só 10 e 7
    'dice_no_win': 'Diesmal nicht! Versuche es beim nächsten Mal!',
    'dice_total_trades': 'Gesamte Trades',
    'dice_total_count': 'Du hast jetzt **{count}** Trades.',
    'dice_cooldown_title': '⏳ Würfel-Cooldown aktiv',
    'dice_cooldown_desc': 'Du musst noch **{minutes} Minuten und {seconds} Sekunden** warten, um erneut zu spielen.',
    'dice_reminder_button': 'Mich erinnern, wenn verfügbar',
    'dice_reminder_set': 'Du erhältst in {minutes} Minuten eine Erinnerung, wenn du wieder spielen kannst.',
    'dice_reminder_message': '🎲 Das Würfel-Minispiel ist wieder verfügbar! Benutze !dice zum Spielen.',
    'dice_already_available': 'Das Minispiel ist bereits verfügbar! Benutze !dice zum Spielen.',

    # Box Game
    'box_game_title': '🎮 Boxenspiel',
    'box_game_desc': '{user}, wähle eine der Boxen unten! **Zwei davon enthalten einen Trade, die anderen sind leer.**',
    'box_game_prize_title': '🎁 Preis',
    'box_game_prize_desc': 'Wenn du eine der richtigen Boxen wählst, gewinnst du 1 Trade!',
    'box_win_title': '🎉 Du hast es geschafft!',
    'box_win_desc': 'Glückwunsch! Du hast Box {box} gewählt und den Preis gewonnen!',
    'box_lose_title': '😢 Diesmal nicht...',
    'box_lose_desc': 'Box {box} war leer. Viel Glück beim nächsten Mal!',
    'box_prize': '🎁 Dein Preis',
    'box_trade_won': 'Du hast 1 Trade gewonnen!',
    'box_total_trades': '💼 Gesamte Trades',
    'box_total_count': 'Du hast jetzt {count} Trades verfügbar.',
    'box_try_again': '🔄 Versuche es erneut',
    'box_cooldown_info': 'Du kannst in 5 Minuten erneut spielen.',
    'box_cooldown_title': '⏳ Cooldown aktiv',
    'box_cooldown_desc': 'Du musst {minutes} Minuten und {seconds} Sekunden warten, um erneut zu spielen.',
    'box_reminder_button': 'Erinnern, wenn verfügbar',
    'box_reminder_set': 'Du erhältst in {minutes} Minuten eine Erinnerung, wenn du erneut spielen kannst.',
    'box_reminder_message': '🎮 Das Boxenspiel ist wieder verfügbar! Benutze !box zum Spielen.',
    'box_already_available': 'Das Spiel ist bereits verfügbar! Benutze !box zum Spielen.',
    'not_your_game': 'Das ist nicht dein Spiel! Benutze !box, um dein eigenes Spiel zu starten.',
    'resetbox_no_member': 'Bitte erwähnen Sie einen Benutzer, um die Abklingzeit des Kisten-Spiels zurückzusetzen.',
    'resetbox_success': 'Die Abklingzeit des Kisten-Spiels von {user} wurde erfolgreich zurückgesetzt.',
    'resetbox_not_on_cooldown': '{user} ist nicht in der Abklingzeit des Kisten-Spiels.',
    'help_box': 'Spielen Sie das Kisten-Spiel, um Trades zu gewinnen.',
    'help_resetbox': 'Setzt die Abklingzeit der Box eines Benutzers zurück.',

    # Slot-System
    'slot_cooldown_title': '🕒 Slot-Abklingzeit aktiv',
    'slot_cooldown_desc': 'Sie müssen noch **{minutes} Minuten und {seconds} Sekunden** warten, um wieder zu spielen.',
    'slot_reminder_button': 'Przypomnij mi, gdy będzie dostępne',
    'not_your_button': 'Ten przycisk nie jest dla Ciebie!',
    'slot_already_available': 'Der Slot ist bereits verfügbar!',
    'slot_reminder_set': 'Fertig! Ich werde Sie benachrichtigen, wenn Sie in etwa {minutes} Minute(n) wieder spielen können.',
    'slot_reminder_message': '⏰ **Erinnerung:** Der Slot ist wieder verfügbar! Verwenden Sie den Befehl `!slot`, um Ihr Glück zu versuchen!',
    'slot_result_title': '🎰 Slot-Ergebnis',
    'slot_result_desc': '{user} hat den Slot gedreht!',
    'slot_machine': 'Spielautomat',
    'slot_result': 'Ergebnis',
    'slot_jackpot': '🏆 JACKPOT! Alle Symbole stimmen überein! Du hast 2 Trades gewonnen!',  # Era 3 trades
    'slot_two_match': '🎉 Zwei Symbole stimmen überein! Du hast 1 Trade gewonnen!',              # Era 2 trades
    'slot_no_match': '😢 Brak kombinacji. Spróbuj ponownie później!',
    'slot_prize': 'Preis',
    'slot_trades_won': 'Sie haben **{count}** Trades gewonnen!',
    'slot_total_trades': 'Gesamte Trades',
    'slot_total_count': 'Sie haben jetzt **{count}** Trades.',
    'resetslot_no_member': '⚠️ Sie müssen ein Mitglied erwähnen, um die Slot-Abklingzeit zurückzusetzen.',
    'resetslot_success': '✅ Slot-Abklingzeit für **{user}** zurückgesetzt.',
    'resetslot_not_on_cooldown': '📭 **{user}** ist nicht in der Slot-Abklingzeit.',
    'help_slot': 'Spielen Sie am Spielautomaten, um Trades zu gewinnen (5 Minuten Abklingzeit).',
    'help_resetslot': 'Setzt die Slot-Abklingzeit eines Benutzers zurück (Admin).',

    # Befehle und Antworten
    'trades_added': '✅ {amount} Trade(s) für {user} hinzugefügt. Aktueller Gesamtbetrag: **{total}**',
    'trades_available': '🎮 Sie haben **{count}** Trade(s) verfügbar.',
    'trades_claimed': '🎁 Sie haben **5 tägliche Trades** erhalten! Sie haben jetzt **{total}** Trade(s).',
    'trades_used': 'ℹ️ Trade verwendet! Sie haben noch **{count}** Trade(s) verfügbar.',
    'generating_trades': '🔄 Generiere einen Trade mit {amount} Tauschvorgängen für {mention}... Details wurden per Privatnachricht gesendet.',

    # Embed-Titel
    'embed_active_trades': '🔍 Ihre aktiven Trades',
    'embed_active_trades_desc': 'Sie haben {count} aktive Trade(s):',
    'embed_trade_status': '🔍 Trade-Status: {code}',
    'embed_help_title': '📚 Trade-Bot Hilfe',
    'embed_help_desc': 'Hier sind die für alle Benutzer verfügbaren Befehle:',
    'embed_admin_help': '🔒 Administrator-Befehle',
    'embed_admin_help_desc': 'Nur für Administratoren verfügbare Befehle:',
    'embed_db_status': '🗄️ Datenbank-Status',

    # Hilfe-Befehle
    'help_listtrades': 'Zeigt an, wie viele Trades Sie verfügbar haben.',
    'help_claimtrade': 'Erhalten Sie Ihre 5 täglichen Trades (alle 24 Stunden verfügbar).',
    'help_usetrade': 'Verwendet einen Ihrer verfügbaren Trades und generiert einen Code zur Verarbeitung der angegebenen Anzahl von Trades.\nBeispiel: `!usetrade 2` - Verwendet einen Trade, um 2 Trades zu verarbeiten.\n⚠️ Sie können nur einen aktiven Trade gleichzeitig haben. Warten Sie auf die Verarbeitung, bevor Sie einen anderen verwenden.',
    'help_help': 'Zeigt diese Hilfenachricht an',
    'help_abort': 'Bricht einen aktiven Trade mit seinem Code ab.',
    'help_lang': 'Legt Ihre bevorzugte Sprache fest. Verfügbare Optionen: de (Deutsch), en (Englisch), es (Spanisch).',

    # Fehler und Warnungen
    'invalid_trades_count': '⚠️ Sie können zwischen 1 und 10 Trades anfordern.',
    'invalid_expiry_time': '⚠️ Die Ablaufzeit muss zwischen 1 und 120 Minuten liegen.',
    'max_active_trades': '⚠️ Sie können maximal 3 aktive Trades haben. Sie haben bereits {count} Trade(s).',
    'system_busy': '⚠️ Das System verarbeitet derzeit zu viele Trades. Bitte versuchen Sie es in einigen Minuten erneut.',
    'invalid_duration': '⚠️ Die Verarbeitungsdauer muss zwischen 1 und 120 Minuten liegen.',
    'no_active_trades': '❌ Sie haben derzeit keine aktiven Trades.',
    'code_not_found': '❌ Code nicht gefunden: {code}',
    'not_your_code': '❌ Dieser Code gehört Ihnen nicht.',
    'trade_amount_invalid': '⚠️ Die Anzahl der Trades muss zwischen 1 und 100 liegen.',
    'no_trades_available': '❌ Sie haben keine verfügbaren Trades. Verwenden Sie `!claimtrade` für tägliche Trades oder fragen Sie einen Administrator.',
    'trade_already_active': '⚠️ Sie haben bereits einen aktiven Trade mit dem Code **{code}**. Warten Sie, bis dieser abgeschlossen ist, bevor Sie einen weiteren verwenden.',
    'not_enough_trades': '❌ Sie haben nicht genug Trades. Sie haben {available} Trade(s) verfügbar, aber {requested} angefordert.',
    'cooldown_active': '⏰ Sie haben Ihre täglichen Trades bereits erhalten. Warten Sie **{hours} Stunden und {minutes} Minuten**, um erneut zu erhalten.',
    'admin_only': '❌ Dieser Befehl ist nur für Administratoren verfügbar.',
    'wrong_channel': '❌ Dieser Befehl muss im Kanal {channel} verwendet werden.',
    'command_unavailable': '❌ Dieser Befehl ist in diesem Kontext nicht verfügbar.',

    # MongoDB und andere
    'db_connected': '✅ MongoDB-Verbindung erfolgreich hergestellt!',
    'db_info': 'Trade-Daten und Benutzer-Abklingzeiten werden in MongoDB gespeichert.',
    'db_disconnected': '⚠️ MongoDB ist nicht verbunden!',
    'db_memory_warning': 'Der Bot arbeitet mit Speicher. Daten gehen beim Neustart des Bots verloren.',
    'db_solution': 'Konfigurieren Sie die Umgebungsvariable `MONGO_URI` in der `.env`-Datei, um die Datenspeicherung zu aktivieren.',
    'db_stats': '- Benutzer mit Trades: {users}\n- Benutzer in Abklingzeit: {cooldowns}\n- Aktive Trades: {active}\n- Benutzer mit laufenden Trades: {in_progress}',

    # Sprachbefehle
    'current_language': 'Ihre aktuelle Sprache ist: **{language}**',
    'available_languages': 'Verfügbare Sprachen: {languages}',
    'invalid_language': '⚠️ Ungültiger Sprachcode: "{code}". Verwenden Sie de, en oder es.',
    'language_updated': '✅ Ihre Sprache wurde auf **{language}** geändert!',
    'specify_trades_amount': '⚠️ Bitte gib die Anzahl der gewünschten Trades an.\nBeispiel: `!usetrade 1`',
    },

    # Italiano
'it': {
    # Messaggi generali
    'trade_code_generated': '🔄 Generazione del codice di trade... Codice: **{code}** (scade in {minutes} minuti)',
    'trade_time_mode': '🔄 Avvio modalità tempo con codice: **{code}** | Elaborazione trades per {duration} minuti (scade in {minutes} min)',
    'trade_processing': '⌛ Elaborazione di {amount} trade(s) con codice: **{code}**... Potrebbe richiedere alcuni secondi.',
    'trade_success': '✅ Trade Configurato con Successo!',
    'trade_success_desc': 'Il tuo codice di trade è stato elaborato per {amount} trade(s).',
    'trade_success_public': '{mention} Hai completato con successo tutti i tuoi trades.',
    'trade_details_sent': 'I dettagli sono stati inviati tramite messaggio privato.',
    'trade_error': '❌ Errore nell\'elaborazione del trade',
    'trade_error_desc': 'Si è verificato un errore durante l\'elaborazione del codice **{code}**.',
    'trade_error_public': '❌ {mention} Si è verificato un errore durante l\'elaborazione del tuo trade. Controlla i tuoi messaggi privati per maggiori dettagli.',
    'trade_by': 'Creato da:',
    'trade_completed': 'Il tuo trade è stato completato con successo.',
    'trade_more_info': 'Per ottenere più trades, partecipa alle attività e agli eventi del server.',
    'abort_no_code': 'Per favore, fornisci il codice del trade che desideri annullare.',
    'abort_success_title': 'Trade Annullato',
    'abort_success_desc': 'Il trade con codice **{code}** è stato annullato con successo.',
    'no_active_codes': 'Non ci sono codici attivi al momento.',
    'active_codes_title': 'Codici Attivi',
    'active_codes_desc': 'Ci sono **{count}** codici attivi nel sistema.',
    'time_remaining': 'Tempo rimanente',
    'minutes': 'minuti',
    'status': 'Stato',
    'help_activecodes': 'Mostra tutti i codici di trade attivi nel sistema.',
    'check_trade_no_member': 'Per favore, menziona un utente da verificare.',
    'check_trade_title': 'Trades di {user}',
    'check_trade_count': 'Numero di trades disponibili',
    'check_trade_active': 'Trade attivo',
    'check_trade_no_active': 'Nessun trade attivo',
    'check_trade_last_claim': 'Ultimo claim giornaliero',
    'check_trade_cooldown': 'In cooldown (Prossimo claim tra: {hours}h {minutes}m)',
    'check_trade_can_claim': 'Puoi fare un nuovo claim',
    'check_trade_never_claimed': 'Non ha mai fatto un claim',
    'check_trade_timestamp': 'Ultimo claim: {time}',
    'help_checktrademember': 'Verifica il numero di trades di un utente e mostra informazioni sul suo ultimo claim giornaliero.',

    'giveaway_new_title': '🎉 Nuovo Giveaway!',
    'giveaway_new_desc': 'Premio: {prize}\n\nVincitori: {winners}\nDurata: {duration} minuti\n\nClicca sul pulsante qui sotto per partecipare!\n{description}',
    'giveaway_footer_id': 'ID: {id}',
    'giveaway_no_permission': 'Non hai il permesso di creare giveaway!',
    'giveaway_only_channel': 'Questo comando può essere usato solo nel canale <#{channel_id}>',
    'giveaway_ended_title': '🎉 Giveaway Terminato',
    'giveaway_ended_desc': 'Premio: {prize}\n\nVincitori: {winners}\n\nOgni vincitore ha ricevuto {prize}!',
    'giveaway_ended_no_participants': 'Nessuno ha partecipato a questo giveaway!',
    'giveaway_deleted': 'Giveaway eliminato con successo!',
    'giveaway_not_found': 'Giveaway non trovato!',
    'giveaway_force_success': 'Giveaway terminato con successo!',
    'giveaway_button_join': 'Partecipa',
    'giveaway_already_joined': 'Stai già partecipando a questo giveaway!',
    'giveaway_join_success': 'Hai partecipato con successo al giveaway! Buona fortuna! 🎉',
    'giveaway_already_ended': 'Questo giveaway è già terminato!',
    'giveaway_dm': '🎉 Complimenti! Hai vinto **{trades}** trades nel giveaway sul server {server}!',

    'bet_vote_success': 'Voto registrato con successo!',
    'bet_already_voted': 'Hai già votato per questa opzione.',
    'bet_closed': 'La scommessa non è aperta alle votazioni.',
    'bet_need_options': 'La scommessa necessita di almeno 2 opzioni.',
    'bet_usage': 'Uso: !bet Titolo Opzione1 Opzione2 [Opzione3 ...]',
    'bet_not_found': 'Scommessa con ID {id} non trovata.',
    'bet_locked': 'La scommessa è già bloccata o terminata.',
    'bet_already_ended': 'La scommessa è già terminata.',

    # DM Trade
    'trades_received_title': '🎁 Hai ricevuto Trades!',
    'trades_received_desc': 'Hai ricevuto {amount} trade(s) dall\'amministratore {admin}. Usa i tuoi trades in {channel}!',
    'current_trades': 'Trades attuali',
    'dm_blocked': '⚠️ Impossibile inviare messaggio privato a {user} - DM bloccati.',
    'dm_error': '⚠️ Errore nell\'invio del messaggio privato a {user}.',
    'trades_added': '✅ Aggiunto {amount} trade(s) per {user}. Totale attuale: {total} trades.',
    'trade_amount_invalid': '❌ Importo trade non valido. Usa tra 1 e 100.',
    'member_not_found': '❌ Membro non trovato o offline.',

    # Dice
    'dice_result_title': '🎲 Risultato dei Dadi',
    'dice_result_desc': '{user} ha lanciato due dadi!',
    'dice_roll': 'Lancio',
    'dice_prize': 'Premio',
    'dice_win_3': '🎉 Complimenti! Hai fatto 12 e vinto **2 trades**!',  # Era 3 trades
    'dice_win_2': 'Ottimo! Hai fatto 11 e vinto **2 trades**!',          # Era 10 o 11, agora só 11
    'dice_win_1': 'Hai fatto 10 o 7 e vinto **1 trade**!',               # Era 7-9, agora só 10 e 7
    'dice_no_win': 'Non questa volta! Riprova la prossima volta!',
    'dice_total_trades': 'Totale Trades',
    'dice_total_count': 'Ora hai **{count}** trades.',
    'dice_cooldown_title': '⏳ Cooldown dei Dadi Attivo',
    'dice_cooldown_desc': 'Devi aspettare ancora **{minutes} minuti e {seconds} secondi** per giocare di nuovo.',
    'dice_reminder_button': 'Ricordami quando disponibile',
    'dice_reminder_set': 'Riceverai un promemoria tra {minutes} minuti quando potrai giocare di nuovo.',
    'dice_reminder_message': '🎲 Il minigioco dei dadi è di nuovo disponibile! Usa !dice per giocare.',
    'dice_already_available': 'Il minigioco è già disponibile! Usa !dice per giocare.',

    # Box Game
    'box_game_title': '🎮 Gioco delle Scatole',
    'box_game_desc': '{user}, scegli una delle scatole qui sotto! **Due di esse contengono un trade, le altre sono vuote.**',
    'box_game_prize_title': '🎁 Premio',
    'box_game_prize_desc': 'Se scegli una delle scatole giuste, vincerai 1 trade!',
    'box_win_title': '🎉 Complimenti!',
    'box_win_desc': 'Hai scelto la scatola {box} e hai vinto il premio!',
    'box_lose_title': '😢 Non questa volta...',
    'box_lose_desc': 'La scatola {box} era vuota. Meglio la prossima volta!',
    'box_prize': '🎁 Il tuo premio',
    'box_trade_won': 'Hai vinto 1 trade!',
    'box_total_trades': '💼 Trade totali',
    'box_total_count': 'Ora hai {count} trade disponibili.',
    'box_try_again': '🔄 Riprova',
    'box_cooldown_info': 'Potrai giocare di nuovo tra 5 minuti.',
    'box_cooldown_title': '⏳ Cooldown attivo',
    'box_cooldown_desc': 'Devi aspettare {minutes} minuti e {seconds} secondi per giocare di nuovo.',
    'box_reminder_button': 'Ricordami quando disponibile',
    'box_reminder_set': 'Riceverai un promemoria tra {minutes} minuti quando potrai giocare di nuovo.',
    'box_reminder_message': '🎮 Il gioco delle scatole è di nuovo disponibile! Usa !box per giocare.',
    'box_already_available': 'Il gioco è già disponibile! Usa !box per giocare.',
    'not_your_game': 'Questo non è il tuo gioco! Usa !box per iniziare il tuo gioco.',
    'resetbox_no_member': 'Per favore, menziona un utente per resettare il cooldown del gioco delle scatole.',
    'resetbox_success': 'Il cooldown del gioco delle scatole di {user} è stato resettato con successo.',
    'resetbox_not_on_cooldown': '{user} non è in cooldown per il gioco delle scatole.',
    'help_box': 'Gioca al gioco delle scatole per vincere trades.',
    'help_resetbox': 'Resetta il cooldown della box di un utente.',

    # Sistema Slot
    'slot_cooldown_title': '🕒 Cooldown dello Slot Attivo',
    'slot_cooldown_desc': 'Devi attendere ancora **{minutes} minuti e {seconds} secondi** per giocare di nuovo.',
    'slot_reminder_button': 'Ricordami quando disponibile',
    'not_your_button': 'Questo pulsante non è per te!',
    'slot_already_available': 'Lo slot è già disponibile per l\'uso!',
    'slot_reminder_set': 'Pronto! Ti avviserò quando potrai giocare di nuovo tra circa {minutes} minuto(i).',
    'slot_reminder_message': '⏰ **Promemoria:** Lo slot è di nuovo disponibile! Usa il comando `!slot` per tentare la fortuna!',
    'slot_result_title': '🎰 Risultato dello Slot',
    'slot_result_desc': '{user} ha girato la slot machine!',
    'slot_machine': 'Slot Machine',
    'slot_result': 'Risultato',
    'slot_jackpot': '🏆 JACKPOT! Tutti i simboli corrispondono! Hai vinto 2 trades!',  # Era 3 trades
    'slot_two_match': '🎉 Due simboli corrispondono! Hai vinto 1 trade!',              # Era 2 trades
    'slot_no_match': '😢 Nessuna combinazione. Riprova più tardi!',
    'slot_prize': 'Premio',
    'slot_trades_won': 'Hai vinto **{count}** trades!',
    'slot_total_trades': 'Totale Trades',
    'slot_total_count': 'Ora hai **{count}** trades.',
    'resetslot_no_member': '⚠️ Devi menzionare un membro per resettare il cooldown dello slot.',
    'resetslot_success': '✅ Cooldown dello slot resettato per **{user}**.',
    'resetslot_not_on_cooldown': '📭 **{user}** n\'est pas en cooldown de slot.',
    'help_slot': 'Gioca alla slot machine per vincere trades (cooldown di 5 minuti).',
    'help_resetslot': 'Resetta il cooldown dello slot di un utente (admin).',

    # Comandi e risposte
    'trades_added': '✅ {amount} trade(s) aggiunto(i) per {user}. Totale attuale: **{total}**',
    'trades_available': '🎮 Hai **{count}** trade(s) disponibile(i).',
    'trades_claimed': '🎁 Hai ricevuto **5 trades giornalieri**! Ora hai **{total}** trade(s).',
    'trades_used': 'ℹ️ Trade utilizzato! Hai ancora **{count}** trade(s) disponibile(i).',
    'generating_trades': '🔄 Generazione di un trade con {amount} scambi per {mention}... Dettagli inviati tramite messaggio privato.',

    # Titoli degli embed
    'embed_active_trades': '🔍 I tuoi Trades Attivi',
    'embed_active_trades_desc': 'Hai {count} trade(s) attivo(i):',
    'embed_trade_status': '🔍 Stato del Trade: {code}',
    'embed_help_title': 'Aiuto del Bot di Trades',
    'embed_help_desc': 'Ecco i comandi disponibili per tutti gli utenti:',
    'embed_admin_help': '🔒 Comandi da Amministratore',
    'embed_admin_help_desc': 'Comandi disponibili solo per gli amministratori:',
    'embed_db_status': '🗄️ Stato del Database',

    # Comandi di aiuto
    'help_listtrades': 'Mostra quanti trades hai disponibili.',
    'help_claimtrade': 'Ricevi i tuoi 5 trades giornalieri (disponibili ogni 24 ore).',
    'help_usetrade': 'Usa uno dei tuoi trades disponibili e genera un codice per elaborare la quantità specificata di trades.\nEsempio: `!usetrade 2` - Usa un trade per elaborare 2 trades.\n⚠️ Puoi avere solo un trade attivo alla volta. Attendi l\'elaborazione prima di usarne un altro.',
    'help_help': 'Mostra questo messaggio di aiuto',
    'help_abort': 'Annulla un trade attivo usando il suo codice.',
    'help_lang': 'Imposta la tua lingua preferita. Opzioni disponibili: it (Italiano), en (Inglese), es (Spagnolo).',

    # Errori e avvisi
    'invalid_trades_count': '⚠️ Puoi richiedere tra 1 e 10 trade.',
    'invalid_expiry_time': '⚠️ Il tempo di scadenza deve essere tra 1 e 120 minuti.',
    'max_active_trades': '⚠️ Puoi avere al massimo 3 trade attivi. Hai già {count} trade.',
    'system_busy': '⚠️ Il sistema sta elaborando troppi trade al momento. Riprova tra qualche minuto.',
    'invalid_duration': '⚠️ La durata dell\'elaborazione deve essere tra 1 e 120 minuti.',
    'no_active_trades': '❌ Non hai trade attivi al momento.',
    'code_not_found': '❌ Codice non trovato: {code}',
    'not_your_code': '❌ Questo codice non ti appartiene.',
    'trade_amount_invalid': '⚠️ Il numero di trade deve essere tra 1 e 100.',
    'no_trades_available': '❌ Non hai trade disponibili. Usa `!claimtrade` per ottenere i trade giornalieri o chiedi a un amministratore.',
    'trade_already_active': '⚠️ Hai già un trade attivo con il codice **{code}**. Attendi che sia completato prima di usarne un altro.',
    'not_enough_trades': '❌ Non hai abbastanza trade. Hai {available} trade disponibili, ma ne hai richiesti {requested}.',
    'cooldown_active': '⏰ Hai già ricevuto i tuoi trade giornalieri. Attendi **{hours} ore e {minutes} minuti** per riceverne altri.',
    'admin_only': '❌ Questo comando è disponibile solo per gli amministratori.',
    'wrong_channel': '❌ Questo comando deve essere usato nel canale {channel}.',
    'command_unavailable': '❌ Questo comando non è disponibile in questo contesto.',

    # MongoDB e altri
    'db_connected': '✅ Connessione a MongoDB stabilita con successo!',
    'db_info': 'I dati dei trades e i cooldown degli utenti vengono salvati in MongoDB.',
    'db_disconnected': '⚠️ MongoDB non è connesso!',
    'db_memory_warning': 'Il bot opera con archiviazione in memoria. I dati verranno persi quando il bot verrà riavviato.',
    'db_solution': 'Configura la variabile d\'ambiente `MONGO_URI` nel file `.env` per abilitare la persistenza dei dati.',
    'db_stats': '- Utenti con trades: {users}\n- Utenti in cooldown: {cooldowns}\n- Trades attivi: {active}\n- Utenti con trades in corso: {in_progress}',

    # Comandi di lingua
    'current_language': 'La tua lingua attuale è: **{language}**',
    'available_languages': 'Lingue disponibili: {languages}',
    'invalid_language': '⚠️ Codice lingua non valido: "{code}". Usa pt, en, es, de, it, fr, pl',
    'language_updated': '✅ La tua lingua è stata cambiata in **{language}**!',
    'specify_trades_amount': '⚠️ Per favore, specifica il numero di trades da usare.\nEsempio: `!usetrade 1`',
    },

    # Polonês
'pl': {
    # Wiadomości ogólne
    'trade_code_generated': '🔄 Generowanie kodu wymiany... Kod: **{code}** (wygasa za {minutes} minut)',
    'trade_time_mode': '🔄 Uruchamianie trybu czasowego z kodem: **{code}** | Przetwarzanie wymian przez {duration} minut (wygasa za {minutes} min)',
    'trade_processing': '⌛ Przetwarzanie {amount} wymian(y) z kodem: **{code}**... Może to zająć kilka sekund.',
    'trade_success': '✅ Wymiana Skonfigurowana Pomyślnie!',
    'trade_success_desc': 'Twój kod wymiany został przetworzony dla {amount} wymian(y).',
    'trade_success_public': '{mention} Pomyślnie zakończyłeś wszystkie swoje wymiany.',
    'trade_details_sent': 'Szczegóły zostały wysłane w wiadomości prywatnej.',
    'trade_error': '❌ Błąd przetwarzania wymiany',
    'trade_error_desc': 'Wystąpił błąd podczas przetwarzania kodu **{code}**.',
    'trade_error_public': '❌ {mention} Wystąpił błąd podczas przetwarzania Twojej wymiany. Sprawdź wiadomości prywatne, aby uzyskać więcej szczegółów.',
    'trade_by': 'Utworzone przez:',
    'trade_completed': 'Twoja wymiana została pomyślnie zakończona.',
    'trade_more_info': 'Aby otrzymać więcej wymian, bierz udział w aktywnościach i wydarzeniach na serwerze.',
    'abort_no_code': 'Proszę podać kod wymiany, którą chcesz anulować.',
    'abort_success_title': 'Wymiana Anulowana',
    'abort_success_desc': 'Wymiana z kodem **{code}** została pomyślnie anulowana.',
    'no_active_codes': 'Obecnie nie ma aktywnych kodów.',
    'active_codes_title': 'Aktywne Kody',
    'active_codes_desc': 'W systemie jest **{count}** aktywnych kodów.',
    'time_remaining': 'Pozostały czas',
    'minutes': 'minuty',
    'status': 'Status',
    'help_activecodes': 'Pokazuje wszystkie aktywne kody wymian w systemie.',
    'check_trade_no_member': 'Proszę oznaczyć użytkownika do sprawdzenia.',
    'check_trade_title': 'Wymiany użytkownika {user}',
    'check_trade_count': 'Liczba dostępnych wymian',
    'check_trade_active': 'Aktywna wymiana',
    'check_trade_no_active': 'Brak aktywnych wymian',
    'check_trade_last_claim': 'Ostatnie dzienne odebranie',
    'check_trade_cooldown': 'W czasie oczekiwania (Następne odebranie za: {hours}h {minutes}m)',
    'check_trade_can_claim': 'Możesz odebrać ponownie',
    'check_trade_never_claimed': 'Nigdy nie odebrał',
    'check_trade_timestamp': 'Ostatnie odebranie: {time}',
    'help_checktrademember': 'Sprawdza liczbę wymian użytkownika i pokazuje informacje o jego ostatnim dziennym odebraniu.',

    'bet_vote_success': 'Głos został pomyślnie zarejestrowany!',
    'bet_already_voted': 'Już zagłosowałeś na tę opcję.',
    'bet_closed': 'Zakład nie jest otwarty do głosowania.',
    'bet_need_options': 'Zakład wymaga co najmniej 2 opcji.',
    'bet_usage': 'Użycie: !bet Tytuł Opcja1 Opcja2 [Opcja3 ...]',
    'bet_not_found': 'Zakład o ID {id} nie został znaleziony.',
    'bet_locked': 'Zakład jest już zablokowany lub zakończony.',
    'bet_already_ended': 'Zakład został już zakończony.',

    'giveaway_new_title': '🎉 Nowy Giveaway!',
    'giveaway_new_desc': 'Nagroda: {prize}\n\nZwycięzcy: {winners}\nCzas trwania: {duration} minut\n\nKliknij przycisk poniżej, aby wziąć udział!\n{description}',
    'giveaway_footer_id': 'ID: {id}',
    'giveaway_no_permission': 'Nie masz uprawnień do tworzenia giveawayów!',
    'giveaway_only_channel': 'Ta komenda może być użyta tylko na kanale <#{channel_id}>',
    'giveaway_ended_title': '🎉 Giveaway Zakończony',
    'giveaway_ended_desc': 'Nagroda: {prize}\n\nZwycięzcy: {winners}\n\nKażdy zwycięzca otrzymał {prize}!',
    'giveaway_ended_no_participants': 'Nikt nie wziął udziału w tym giveawayu!',
    'giveaway_deleted': 'Giveaway został pomyślnie usunięty!',
    'giveaway_not_found': 'Giveaway nie został znaleziony!',
    'giveaway_force_success': 'Giveaway został pomyślnie zakończony!',
    'giveaway_button_join': 'Weź udział',
    'giveaway_already_joined': 'Już bierzesz udział w tym giveawayu!',
    'giveaway_join_success': 'Pomyślnie dołączyłeś do giveawayu! Powodzenia! 🎉',
    'giveaway_already_ended': 'Ten giveaway już się zakończył!',
    'giveaway_dm': '🎉 Gratulacje! Wygrałeś **{trades}** trades w losowaniu na serwerze {server}!',

    # DM Trade
    'trades_received_title': '🎁 Otrzymałeś Trades!',
    'trades_received_desc': 'Otrzymałeś {amount} trade(s) od administratora {admin}. Użyj swoich trades w {channel}!',
    'current_trades': 'Aktualne Trades',
    'dm_blocked': '⚠️ Nie można wysłać wiadomości prywatnej do {user} - DM zablokowane.',
    'dm_error': '⚠️ Błąd podczas wysyłania wiadomości prywatnej do {user}.',
    'trades_added': '✅ Dodano {amount} trade(s) dla {user}. Aktualny całkowity: {total} trades.',
    'trade_amount_invalid': '❌ Nieprawidłowa ilość trade. Użyj między 1 a 100.',
    'member_not_found': '❌ Członek nie znaleziony lub offline.',

    # Dice
    'dice_result_title': '🎲 Wynik Kości',
    'dice_result_desc': '{user} rzucił dwiema kośćmi!',
    'dice_roll': 'Rzut',
    'dice_prize': 'Nagroda',
    'dice_win_3': '🎉 Gratulacje! Wyrzuciłeś 12 i wygrałeś **2 wymiany**!',  # Era 3 trades
    'dice_win_2': 'Świetnie! Wyrzuciłeś 11 i wygrałeś **2 wymiany**!',        # Era 10 lub 11, agora só 11
    'dice_win_1': 'Wyrzuciłeś 10 lub 7 i wygrałeś **1 wymianę**!',            # Era 7-9, agora só 10 e 7
    'dice_no_win': 'Tym razem nie! Spróbuj ponownie następnym razem!',
    'dice_total_trades': 'Łączna liczba wymian',
    'dice_total_count': 'Masz teraz **{count}** wymian.',
    'dice_cooldown_title': '⏳ Aktywny cooldown kości',
    'dice_cooldown_desc': 'Musisz poczekać jeszcze **{minutes} minut i {seconds} sekund**, aby zagrać ponownie.',
    'dice_reminder_button': 'Przypomnij mi, gdy będzie dostępne',
    'dice_reminder_set': 'Otrzymasz przypomnienie za {minutes} minut, gdy będziesz mógł zagrać ponownie.',
    'dice_reminder_message': '🎲 Minigra z kośćmi jest ponownie dostępna! Użyj !dice, aby zagrać.',
    'dice_already_available': 'Minigra jest już dostępna! Użyj !dice, aby zagrać.',

    # Gra w Pudełka
    'box_game_title': '🎮 Gra w Skrzynki',
    'box_game_desc': '{user}, wybierz jedną z poniższych skrzynek! **Dwie z nich zawierają trade, pozostałe są puste.**',
    'box_game_prize_title': '🎁 Nagroda',
    'box_game_prize_desc': 'Jeśli wybierzesz jedną z właściwych skrzynek, wygrasz 1 trade!',
    'box_win_title': '🎉 Udało się!',
    'box_win_desc': 'Gratulacje! Wybrałeś skrzynkę {box} i wygrałeś nagrodę!',
    'box_lose_title': '😢 Tym razem nie...',
    'box_lose_desc': 'Skrzynka {box} była pusta. Powodzenia następnym razem!',
    'box_prize': '🎁 Twoja nagroda',
    'box_trade_won': 'Wygrałeś 1 trade!',
    'box_total_trades': '💼 Łączna liczba trade',
    'box_total_count': 'Masz teraz {count} trade dostępnych.',
    'box_try_again': '🔄 Spróbuj ponownie',
    'box_cooldown_info': 'Będziesz mógł zagrać ponownie za 5 minut.',
    'box_cooldown_title': '⏳ Aktywny cooldown',
    'box_cooldown_desc': 'Musisz poczekać {minutes} minut i {seconds} sekund, aby zagrać ponownie.',
    'box_reminder_button': 'Przypomnij, gdy dostępne',
    'box_reminder_set': 'Otrzymasz przypomnienie za {minutes} minut, gdy będziesz mógł zagrać ponownie.',
    'box_reminder_message': '🎮 Gra w skrzynki jest ponownie dostępna! Użyj !box, aby zagrać.',
    'box_already_available': 'Gra jest już dostępna! Użyj !box, aby zagrać.',
    'not_your_game': 'To nie jest twoja gra! Użyj !box, aby rozpocząć własną grę.',
    'resetbox_no_member': 'Proszę oznaczyć użytkownika, aby zresetować czas oczekiwania gry w pudełka.',
    'resetbox_success': 'Czas oczekiwania gry w pudełka dla {user} został pomyślnie zresetowany.',
    'resetbox_not_on_cooldown': '{user} nie jest w czasie oczekiwania gry w pudełka.',
    'help_box': 'Graj w grę w pudełka, aby wygrać wymiany.',
    'help_resetbox': 'Resetuje czas oczekiwania pudełka użytkownika.',

    # System Slotów
    'slot_cooldown_title': '🕒 Aktywny czas oczekiwania slotów',
    'slot_cooldown_desc': 'Musisz poczekać jeszcze **{minutes} minut i {seconds} sekund**, aby zagrać ponownie.',
    'slot_reminder_button': 'Przypomnij mi, gdy będzie dostępne',
    'not_your_button': 'Ten przycisk nie jest dla Ciebie!',
    'slot_already_available': 'Sloty są już dostępne do użycia!',
    'slot_reminder_set': 'Gotowe! Powiadomię Cię, gdy będziesz mógł zagrać ponownie za około {minutes} minut(y).',
    'slot_reminder_message': '⏰ **Przypomnienie:** Sloty są ponownie dostępne! Użyj komendy `!slot`, aby spróbować szczęścia!',
    'slot_result_title': '🎰 Wynik Slotów',
    'slot_result_desc': '{user} zakręcił maszyną do gry!',
    'slot_machine': 'Maszyna do Gry',
    'slot_result': 'Wynik',
    'slot_jackpot': '🏆 JACKPOT! Wszystkie symbole pasują! Wygrałeś 2 wymiany!',  # Era 3 trades
    'slot_two_match': '🎉 Dwa symbole pasują! Wygrałeś 1 wymianę!',                  # Era 2 trades
    'slot_no_match': '😢 Brak kombinacji. Spróbuj ponownie później!',
    'slot_prize': 'Nagroda',
    'slot_trades_won': 'Wygrałeś **{count}** wymian(y)!',
    'slot_total_trades': 'Gesamte Trades',
    'slot_total_count': 'Sie haben jetzt **{count}** Trades.',
    'resetslot_no_member': '⚠️ Musisz oznaczyć członka, aby zresetować czas oczekiwania slotów.',
    'resetslot_success': '✅ Czas oczekiwania slotów dla **{user}** został zresetowany.',
    'resetslot_not_on_cooldown': '📭 **{user}** nie jest w czasie oczekiwania slotów.',
    'help_slot': 'Graj w automaty, aby wygrać wymiany (5 Minuten Abklingzeit).',
    'help_resetslot': 'Resetuje czas oczekiwania slotów użytkownika (admin).',

    # Komendy i odpowiedzi
    'trades_added': '✅ {amount} wymian(y) dodano dla {user}. Aktualna suma: **{total}**',
    'trades_available': '🎮 Masz **{count}** dostępnych wymian(y).',
    'trades_claimed': '🎁 Otrzymałeś **5 dziennych wymian**! Masz teraz **{total}** wymian(y).',
    'trades_used': 'ℹ️ Wykorzystano wymianę! Masz jeszcze **{count}** dostępnych wymian(y).',
    'generating_trades': '🔄 Generowanie wymiany z {amount} zamianami dla {mention}... Szczegóły wysłano w wiadomości prywatnej.',

    # Tytuły embedów
    'embed_active_trades': '🔍 Twoje Aktywne Wymiany',
    'embed_active_trades_desc': 'Masz {count} aktywnych wymian(y):',
    'embed_trade_status': '🔍 Status Wymiany: {code}',
    'embed_help_title': '📚 Pomoc Bota Wymian',
    'embed_help_desc': 'Oto komendy dostępne dla wszystkich użytkowników:',
    'embed_admin_help': '🔒 Komendy Administratora',
    'embed_admin_help_desc': 'Komendy dostępne tylko dla administratorów:',
    'embed_db_status': '🗄️ Status Bazy Danych',

    # Komendy pomocy
    'help_listtrades': 'Pokazuje, ile masz dostępnych wymian.',
    'help_claimtrade': 'Odbierz swoje 5 dziennych wymian (dostępne co 24 godziny).',
    'help_usetrade': 'Użyj jednej ze swoich dostępnych wymian i wygeneruj kod do przetworzenia określonej liczby wymian.\nPrzykład: `!usetrade 2` - Używa jednej wymiany do przetworzenia 2 wymian.\n⚠️ Możesz mieć tylko jedną aktywną wymianę naraz. Poczekaj na przetworzenie, zanim użyjesz kolejnej.',
    'help_help': 'Wyświetla ten komunikat pomocy',
    'help_abort': 'Anuluje aktywną wymianę używając jej kodu.',
    'help_lang': 'Ustawia Twój preferowany język. Dostępne opcje: pl (Polski), en (Angielski), es (Hiszpański).',

    # Błędy i ostrzeżenia
    'invalid_trades_count': '⚠️ Możesz zażądać od 1 do 10 wymian.',
    'invalid_expiry_time': '⚠️ Czas wygaśnięcia musi wynosić od 1 do 120 minut.',
    'max_active_trades': '⚠️ Możesz mieć maksymalnie 3 aktywne wymiany. Masz już {count} wymian(y).',
    'system_busy': '⚠️ System przetwarza zbyt wiele wymian w tej chwili. Spróbuj ponownie za kilka minut.',
    'invalid_duration': '⚠️ Czas przetwarzania musi wynosić od 1 do 120 minut.',
    'no_active_trades': '❌ Nie masz aktywnych wymian w tej chwili.',
    'code_not_found': '❌ Nie znaleziono kodu: {code}',
    'not_your_code': '❌ Ten kod nie należy do Ciebie.',
    'trade_amount_invalid': '⚠️ Liczba wymian musi wynosić od 1 do 100.',
    'no_trades_available': '❌ Nie masz dostępnych wymian. Użyj `!claimtrade`, aby otrzymać dzienne wymiany lub poproś administratora.',
    'trade_already_active': '⚠️ Masz już aktywną wymianę z kodem **{code}**. Poczekaj, aż zostanie zakończona, zanim użyjesz kolejnej.',
    'not_enough_trades': '❌ Nie masz wystarczającej liczby wymian. Masz {available} wymian(y) dostępnych, ale zażądałeś {requested}.',
    'cooldown_active': '⏰ Już otrzymałeś swoje dzienne wymiany. Poczekaj **{hours} godzin i {minutes} minut**, aby otrzymać ponownie.',
    'admin_only': '❌ Ta komenda jest dostępna tylko dla administratorów.',
    'wrong_channel': '❌ Ta komenda musi być użyta na kanale {channel}.',
    'command_unavailable': '❌ Ta komenda nie jest dostępna w tym kontekście.',

    # MongoDB i inne
    'db_connected': '✅ Połączenie z MongoDB nawiązane pomyślnie!',
    'db_info': 'Dane wymian i czasy oczekiwania użytkowników są przechowywane w MongoDB.',
    'db_disconnected': '⚠️ MongoDB nie jest połączone!',
    'db_memory_warning': 'Bot działa z pamięcią. Dane zostaną utracone po ponownym uruchomieniu bota.',
    'db_solution': 'Skonfiguruj zmienną środowiskową `MONGO_URI` w pliku `.env`, aby włączyć przechowywanie danych.',
    'db_stats': '- Użytkownicy z wymianami: {users}\n- Użytkownicy w czasie oczekiwania: {cooldowns}\n- Aktywne wymiany: {active}\n- Użytkownicy z trwającymi wymianami: {in_progress}',

    # Komendy językowe
    'current_language': 'Twój obecny język to: **{language}**',
    'available_languages': 'Dostępne języki: {languages}',
    'invalid_language': '⚠️ Nieprawidłowy kod języka: "{code}". Użyj pt, en, es, de, it, fr, pl',
    'language_updated': '✅ Twój język został zmieniony na **{language}**!',
    'specify_trades_amount': '⚠️ Podaj liczbę trade\'ów do użycia.\nPrzykład: `!usetrade 1`',
    },
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