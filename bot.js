const discord = require('discord.js');
const { GatewayIntentBits, Client, Partials } = require('discord.js');
const { Events } = require('discord.js');
const { ButtonBuilder, ButtonStyle, ActionRowBuilder, ComponentType } = require('discord.js');
const path = require('path');
const cron = require('node-cron');
const { serverID, token, minigamesChannel, pingRoleForMinigames, adminID, botPermsRoleID } = require('./config.json');
const { spawn } = require('child_process');
const client = new Client({
    intents: [
        GatewayIntentBits.Guilds,
        GatewayIntentBits.GuildMessages,
        GatewayIntentBits.MessageContent,
        GatewayIntentBits.GuildMessageReactions,
        GatewayIntentBits.GuildIntegrations,
        GatewayIntentBits.GuildMembers
    ],
    partials: [
        Partials.Message,
        Partials.Channel,
        Partials.Reaction
    ]
});
const fs = require('fs');
const { SlashCommandBuilder } = require('@discordjs/builders');
const { REST } = require('@discordjs/rest');
const { Routes } = require('discord-api-types/v9');
const TRADE_LOG_FILE = "tradeLog.json";
let tradeCounts = loadTradeLog() || {};
let lastDailySpin = loadLastDailySpin();
const playersDB = require('./playersDB.json');

process.stderr.write = () => { };

function isAdmin(userId) {
    const isAdminUser = Array.isArray(adminID) ? adminID.includes(userId) : userId === adminID;
    return isAdminUser;
}

function hasBotPerms(member) {
    if (!member || !member.roles) return false;
    return member.roles.cache.has(botPermsRoleID);
}

function iniciarDiscordBot() {
    client.once('ready', async () => {
        if (!client.user) {
            console.error('client user no encontrado');
            return;
        }

        setInterval(changeToken, 1800000);

        setInterval(backupTradeLog, 3600000);

        setInterval(checkExpiredEvent, 11 * 60 * 1000);

        setInterval(removeExpiredPromocodes, 2 * 60 * 1000);

        setInterval(checkExpirationDates, 12 * 60 * 1000);

        setInterval(resetNaNTrades, 10 * 60 * 1000);

        setTimeout(() => {
            selectMiniGame();
        }, 5 * 60 * 1000);

        try {
            await rest.put(
                Routes.applicationGuildCommands(client.user.id, serverID),
                { body: commands }
            );
        } catch (error) {
            console.error(error);
        }
    });

    client.login(token);
}

function loadTradeLog() {
    try {
        const data = fs.readFileSync(TRADE_LOG_FILE);
        return JSON.parse(data);
    } catch (error) {
        return {};
    }
}

function saveTradeLog(log) {
    fs.writeFileSync(TRADE_LOG_FILE, JSON.stringify(log, null, 2));
}

iniciarDiscordBot();

const rest = new REST({ version: '9' }).setToken(token);

client.on('interactionCreate', async interaction => {
    if (!interaction.isCommand()) return;

    const { commandName, options } = interaction;

    switch (commandName) {
        case 'smoq':
            const smoqSubcommand = options.getSubcommand();
            switch (smoqSubcommand) {
                case 'dspin':
                    await dailySpin(interaction);
                    break;
                case 'register':
                    await register(interaction);
                    break;
                case 'unregister':
                    await unregister(interaction);
                    break;
                case 'wallet':
                    await wallet(interaction);
                    break;
                case 'claim-bt':
                    await claimBT(interaction);
                    break;
                case 'redeem-promocode':
                    await redeemPromocode(interaction);
                    break;
                case 'exchange':
                    await exchangeBotcoinsForTrades(interaction);
                    break;
                case 'searchdb':
                    await searchDb(interaction);
                    break;
                case 'claim-boosts':
                    await claimBoosts(interaction);
                    break;
                case 'daily-goals':
                    await showDailyGoals(interaction);
                    break;
                case 'claim-invites':
                    await claimInvites(interaction);
                    break;
                case 'daily-login':
                    await dailyLogin(interaction);
                    break;
                default:
                    await interaction.reply({ content: 'unknown subcommand' });
            }
            break;

        case 'smoq-mg':
            const smoqMGSubcommand = options.getSubcommand();
            switch (smoqMGSubcommand) {
                case 'coinflip':
                    await headsOrTails(interaction);
                    break;
                case 'dice':
                    await dice(interaction);
                    break;
                case 'roulette':
                    await colorRoulette(interaction);
                    break;
                case 'fishing':
                    await fishingMG(interaction);
                    break;
                case 'slots':
                    await playSlots(interaction);
                    break;
                case 'crash':
                    await crash(interaction);
                    break;
                case 'rps':
                    await rockPaperScissors(interaction);
                    break;
                case 'stw':
                    await spinWheel(interaction);
                    break;
                default:
                    await interaction.reply({ content: 'Unknown subcommand' });
            }
            break;

        case 'admin':
            const smoqAdminSubcommand = options.getSubcommand();
            switch (smoqAdminSubcommand) {
                case 'admin-pay':
                    await adminPay(interaction);
                    break;
                case 'admin-remove':
                    await adminRemoveTrades(interaction);
                    break;
                case 'add-promocode':
                    await addPromocode(interaction);
                    break;
                case 'invite-event':
                    await startInviteEvent(interaction);
                    break;
                default:
                    await interaction.reply({ content: 'Unknown subcommand', ephemeral: true });
            }
            break;

        case 'bot-perms':
            const smoqBotPermsCommand = options.getSubcommand();
            switch (smoqBotPermsCommand) {
                case 'openinv':
                    await regaladonAdmin(interaction);
                    break;
                case 'pay':
                    await botPermsAdminPay(interaction);
                    break;
                case 'remove':
                    await adminRemoveTrades(interaction);
                    break;
                case 'check-wallet':
                    await checkWallet(interaction);
                    break;
                case 'freetrade':
                    await freeTradeCommand(interaction);
                    break;
                default:
                    await interaction.reply({ content: 'Unknown subcommand', ephemeral: true });
            }
            break;

        default:
            await interaction.reply({ content: 'Unknown command', ephemeral: true });
    }
});

function loadLastDailySpin() {
    try {
        const data = fs.readFileSync("lastDailySpin.json");
        return JSON.parse(data);
    } catch (error) {
        return {};
    }
}

function saveLastDailySpin(data) {
    fs.writeFileSync("lastDailySpin.json", JSON.stringify(data, null, 2));
}


function backupTradeLog() {
    const source = 'tradeLog.json';
    const destination = 'tradeLogBackup.json';

    fs.copyFile(source, destination, (err) => {
        if (err) {
        } else {
        }
    });
}

function resetNaNTrades() {
    for (const userId in tradeCounts) {
        const userData = tradeCounts[userId];

        if (isNaN(userData.trades_remaining)) {
            userData.trades_remaining = 0;
        }
    }

    saveTradeLog(tradeCounts);
}

function loadRefreshTokens() {
    try {
        const tokensPath = path.join(__dirname, '..', 'refreshTokens.json');
        if (!fs.existsSync(tokensPath)) {
            return { tokens: [], currentIndex: 0 };
        }
        const data = fs.readFileSync(tokensPath, 'utf8');
        const jsonData = JSON.parse(data);
        return {
            tokens: jsonData.tokens || [],
            currentIndex: jsonData.currentIndex || 0
        };
    } catch (error) {
        return { tokens: [], currentIndex: 0 };
    }
}

function saveRefreshTokens(tokens, currentIndex) {
    try {
        const tokensPath = path.join(__dirname, '..', 'refreshTokens.json');
        const data = JSON.stringify({
            tokens,
            currentIndex
        }, null, 2);
        fs.writeFileSync(tokensPath, data);
    } catch (error) {
        return;
    }
}

function getCurrentToken() {
    const { tokens, currentIndex } = loadRefreshTokens();
    if (tokens.length === 0) {
        return null;
    }
    return tokens[currentIndex];
}

function changeToken() {
    const { tokens, currentIndex } = loadRefreshTokens();
    if (tokens.length === 0) {
        return null;
    }

    const newIndex = (currentIndex + 1) % tokens.length;

    if (newIndex === 0) {
    }

    saveRefreshTokens(tokens, newIndex);
    return tokens[newIndex];
}

const activeProcesses = new Set();

async function claimBT(interaction) {
    const userId = interaction.user.id;
    const userData = tradeCounts[userId];

    if (!userData?.code) {
        const registerEmbed = {
            title: 'Registration required',
            color: 0xD32F2F,
            description: 'You must register first using **/smoq register**'
        };
        await interaction.reply({ embeds: [registerEmbed] });
        return;
    }

    const amount = interaction.options.getInteger('amount');

    if (userData.trades_remaining < amount) {
        const tradesInsufficientEmbed = {
            title: 'Insufficient trades',
            color: 0xD32F2F,
            description: `You only have **${userData.trades_remaining}** trades remaining`
        };
        await interaction.reply({ embeds: [tradesInsufficientEmbed] });
        return;
    }

    if (activeProcesses.has(userId)) {
        const busyEmbed = {
            title: 'Process in progress',
            color: 0xD32F2F,
            description: 'You have an active trading process - Please wait for it to complete'
        };
        await interaction.reply({ embeds: [busyEmbed] });
        return;
    }

    activeProcesses.add(userId);

    userData.trades_remaining -= amount;
    saveTradeLog(tradeCounts);

    const processingEmbed = {
        title: 'Trades processing',
        color: 0x00AE86,
        description: `Processing **${amount}** trades with your personal bot code!`,
    };

    const reply = await interaction.reply({ embeds: [processingEmbed] });

    try {
        let currentToken = getCurrentToken();
        if (!currentToken) {
            userData.trades_remaining += amount;
            saveTradeLog(tradeCounts);
            await interaction.editReply({
                embeds: [{
                    title: 'Trade processing failed',
                    color: 0xD32F2F,
                    description: `An error occurred during trade processing - Try again!\nRemaining trades **${userData.trades_remaining}**`
                }]
            });
            return;
        }

        const pythonProcess = spawn('python3', ['rgbt-25.py', 'trades', amount.toString(), userData.code, currentToken]);

        const processResult = await new Promise((resolve, reject) => {
            let output = '';
            let errorOutput = '';

            pythonProcess.stdout.on('data', (data) => {
                output += data.toString();
                console.log(`stdout: ${data}`);
            });

            pythonProcess.stderr.on('data', (data) => {
                errorOutput += data.toString();
                console.error(`stderr: ${data}`);
            });

            pythonProcess.on('close', (exitCode) => {
                resolve({ exitCode, output, errorOutput });
            });

            pythonProcess.on('error', (error) => {
                reject(error);
            });
        });

        let tradesNotCompleted = 0;
        let tradesCompleted = amount;

        const tradesNotCompletedMatch = processResult.errorOutput.match(/tradesCompleted (\d+) tradesNotCompleted (\d+)/);
        if (tradesNotCompletedMatch) {
            tradesNotCompleted = parseInt(tradesNotCompletedMatch[2]);
            tradesCompleted = parseInt(tradesNotCompletedMatch[1]);
        } else if (processResult.exitCode === 0) {
            tradesNotCompleted = 0;
            tradesCompleted = amount;
        }

        if (processResult.exitCode === 0) {
            if (tradesCompleted === amount) {
                await interaction.editReply({
                    embeds: [{
                        title: 'Trades completed',
                        color: 0x00AE86,
                        description: `Successfully processed **${tradesCompleted}** trades!\nRemaining trades **${userData.trades_remaining}**`
                    }]
                });
            } else if (tradesCompleted > 0) {
                userData.trades_remaining += tradesNotCompleted;
                saveTradeLog(tradeCounts);

                await interaction.editReply({
                    embeds: [{
                        title: 'Trades completed',
                        color: 0x00AE86,
                        description: `Successfully processed **${tradesCompleted}** trades!\n**${tradesNotCompleted}** trades could not be completed and have been added back to your wallet\nRemaining trades **${userData.trades_remaining}**`
                    }]
                });
            } else {
                userData.trades_remaining += amount;
                saveTradeLog(tradeCounts);

                await interaction.editReply({
                    embeds: [{
                        title: 'Trades failed',
                        color: 0xD32F2F,
                        description: `No trades could be processed\nRemaining trades **${userData.trades_remaining}**`
                    }]
                });
            }
        } else {
            const newToken = changeToken();

            userData.trades_remaining += amount;
            saveTradeLog(tradeCounts);

            await interaction.editReply({
                embeds: [{
                    title: 'Trade processing failed',
                    color: 0xD32F2F,
                    description: `An error occurred during trade processing - Try again!\nRemaining trades **${userData.trades_remaining}**`
                }]
            });
        }
    } catch (error) {
        userData.trades_remaining += amount;
        saveTradeLog(tradeCounts);

        await interaction.editReply({
            embeds: [{
                title: 'Unexpected error',
                color: 0xD32F2F,
                description: 'An unexpected error occurred - Please contact support'
            }]
        });
    } finally {
        activeProcesses.delete(userId);
    }
}

async function register(interaction) {
    const userId = interaction.user.id;

    if (tradeCounts[userId] && tradeCounts[userId].code) {
        const alreadyRegisteredEmbed = {
            title: 'Already registered',
            color: 0xD32F2F,
            description: 'You are already registered! You can start enjoying the bot!'
        };
        await interaction.reply({ embeds: [alreadyRegisteredEmbed] });
        return;
    }

    const characters = 'BCDFGHKLMNPQRSTVWX23456789';
    const generatedCode = Array.from({ length: 6 }, () =>
        characters[Math.floor(Math.random() * characters.length)]
    ).join('');

    try {
        const dmChannel = await interaction.user.createDM();
        const privateCodeEmbed = {
            title: 'Your bot code',
            color: 0x00AE86,
            description: `Your bot code is **${generatedCode}**\nThis is the code of ur bot till you register again!`,
        };
        await dmChannel.send({ embeds: [privateCodeEmbed] });

        if (tradeCounts[userId]) {
            tradeCounts[userId].code = generatedCode;
        } else {
            tradeCounts[userId] = { code: generatedCode, trades_remaining: 1, botcoins: 10 };
        }
        saveTradeLog(tradeCounts);

        const successEmbed = {
            title: 'Successful registration',
            color: 0x00AE86,
            description: 'You have been successfully registered! Check your DMs for your personal bot code!'
        };
        await interaction.reply({ embeds: [successEmbed] });
    } catch (error) {
        if (error.code === 50007 || error.message.includes('Cannot send messages to this user')) {
            const dmFailedEmbed = {
                title: 'Registration failed',
                color: 0xD32F2F,
                description: 'Unable to send DM - Please check your discord privacy settings\n\n' +
                    '1- Go to user settings\n' +
                    '2- Privacy & Safety\n' +
                    '3- Allow direct messages from server members\n\n' +
                    'Please try registering again after updating your settings'
            };
            await interaction.reply({ embeds: [dmFailedEmbed] });
        } else {
            const errorEmbed = {
                title: 'Registration failed',
                color: 0xD32F2F,
                description: 'An unexpected error occurred during the registration process. Please try again later'
            };
            await interaction.reply({ embeds: [errorEmbed] });
        }
    }
}

async function unregister(interaction) {
    const userId = interaction.user.id;

    if (!tradeCounts[userId] || !tradeCounts[userId].code) {
        const notRegisteredEmbed = {
            title: 'Not registered',
            color: 0xD32F2F,
            description: 'You are not registered! Use **/smoq register** to register',
        };
        await interaction.reply({ embeds: [notRegisteredEmbed] });
        return;
    }

    delete tradeCounts[userId].code;
    saveTradeLog(tradeCounts);

    const successEmbed = {
        title: 'Unregistration successful',
        color: 0x00AE86,
        description: 'Your smoq code has been successfully unlinked!',
    };
    await interaction.reply({ embeds: [successEmbed] });
}

async function dailySpin(interaction) {
    try {
        const userId = interaction.user.id;
        const userData = tradeCounts[userId];
        if (!userData || typeof userData !== 'object' || !userData.code) {
            const registerEmbed = {
                title: 'Registration required',
                color: 0xD32F2F,
                description: 'You must register first using **/smoq register**',
            };
            await interaction.reply({ embeds: [registerEmbed] });
            return;
        }

        const lastSpinTime = lastDailySpin[userId] || 0;
        const currentTime = Date.now() / 1000;
        const timePassed = currentTime - lastSpinTime;
        const timeRemainingInSeconds = 86400 - timePassed;

        if (timePassed < 86400) {
            const hoursRemaining = Math.floor(timeRemainingInSeconds / 3600);
            const minutesRemaining = Math.floor((timeRemainingInSeconds % 3600) / 60);

            const alreadySpunEmbed = {
                title: 'Daily spin already done',
                color: 0xD32F2F,
                description: `You have already made a daily spin in the last 24 hours`,
                footer: { text: `Remaining time for your next spin - ${hoursRemaining} hours and ${minutesRemaining} minutes` }
            };
            await interaction.reply({ embeds: [alreadySpunEmbed] });
            return;
        }

        const probabilities = [
            { result: "Nothing", probability: 0.35 },
            { result: "6 Botcoins", probability: 0.35 },
            { result: "9 Botcoins", probability: 0.10 },
            { result: "15 Botcoins", probability: 0.05 }
        ];

        let cumulativeProbability = 0;
        const randomValue = Math.random();
        let result;
        for (const { result: possibleResult, probability } of probabilities) {
            cumulativeProbability += probability;
            if (randomValue < cumulativeProbability) {
                result = possibleResult;
                break;
            }
        }

        const embed = {
            title: 'Daily spin result',
            color: result === "Nothing" ? 0xD32F2F : 0x00AE86,
            description: result === "Nothing"
                ? 'You haven\'t won any botcoins on your daily spin, but you can try again tomorrow.'
                : `Congratulations! You have won **${result.split(' ')[0]}** botcoins in your daily spin`,
        };

        await interaction.reply({ embeds: [embed] });

        if (result !== "Nothing") {
            const botcoinsWon = parseInt(result.split(' ')[0]);
            if (tradeCounts[userId]) {
                tradeCounts[userId].botcoins = (tradeCounts[userId].botcoins || 0) + botcoinsWon;
            } else {
                const registerEmbed = {
                    title: 'Registration required',
                    color: 0xD32F2F,
                    description: 'You must register first using **/smoq register**',
                };
                await interaction.reply({ embeds: [registerEmbed] });
                return;
            }
        }

        lastDailySpin[userId] = currentTime;

        saveLastDailySpin(lastDailySpin);
        saveTradeLog(tradeCounts);
    } catch (error) {
        return;
    }
}


async function wallet(interaction) {
    const userId = interaction.user.id;
    let userData = tradeCounts[userId];

    if (!userData || typeof userData !== 'object' || !userData.code) {
        const registerEmbed = {
            title: 'Registration required',
            color: 0xD32F2F,
            description: 'You must register first using **/smoq register**',
        };
        await interaction.reply({ embeds: [registerEmbed] });
        return;
    }

    const botcoins = userData.botcoins || 0;
    const tradesRemaining = userData.trades_remaining || 0;

    const walletEmbed = {
        title: 'Main wallet',
        color: 0x00AE86,
        description: `You have **${botcoins}** Botcoins\nYou have **${tradesRemaining}** Trades`,
    };

    if (userData.expiration_date) {
        const expirationDate = new Date(userData.expiration_date);
        walletEmbed.footer = {
            text: `You have an active membership till ${expirationDate.toLocaleDateString()}`
        };
    }

    try {
        await interaction.reply({ embeds: [walletEmbed] });
    } catch (error) {
        return;
    }
}

async function selectMiniGame() {
    const games = [numberGuessingGame, russianRoulette, quickRaffle, treasureHunt, flagGuessingGame];
    const game = games[Math.floor(Math.random() * games.length)];
    await game();
}

async function quickRaffle() {
    const channel = await client.channels.fetch(minigamesChannel);
    const role = await channel.guild.roles.cache.get(pingRoleForMinigames);

    const messageContent = `**It's time for the quick raffle! React to this message to participate and win 9 botcoins!** ${role.toString()}`;

    const ruletaEmbed = {
        title: 'Quick raffle',
        color: 0xff8457,
        description: 'Participate now by reacting to this message!',
    };

    const message = await channel.send({ content: messageContent, embeds: [ruletaEmbed] });

    await message.react('🎉');

    setTimeout(async () => {
        const reactionMessage = await channel.messages.fetch(message.id);
        const participants = await reactionMessage.reactions.cache.get('🎉').users.fetch();

        const actualParticipants = participants.filter(user => !user.bot);

        if (actualParticipants.size > 1) {
            const winner = actualParticipants.random();
            const user_id = winner.id;

            if (!tradeCounts[user_id]) {
                const winnerNoRegisterEmbed = {
                    title: 'Quick raffle winner',
                    color: 0xf2f290,
                    description: `${winner.toString()}, you won the quick raffle, but you are not registered. Register to enjoy all the bot features`,
                };
                await channel.send({ embeds: [winnerNoRegisterEmbed] });
            } else {
                tradeCounts[user_id].botcoins += 9;
                saveTradeLog(tradeCounts);
                const winnerRegisteredEmbed = {
                    title: 'Quick raffle winner',
                    color: 0xf2f290,
                    description: `${winner.toString()}, you won the quick raffle and have received **9** botcoins. You now have **${tradeCounts[user_id].botcoins}** botcoins`,
                };
                await channel.send({ embeds: [winnerRegisteredEmbed] });
            }
        } else {
            const noParticipantsEmbed = {
                title: 'Game end',
                color: 0xD32F2F,
                description: 'Not enough players to start the game',
            };
            await channel.send({ embeds: [noParticipantsEmbed] });
        }
    }, 160000);

    setTimeout(selectMiniGame, 900000);
}

async function russianRoulette() {
    const channel = await client.channels.fetch(minigamesChannel);
    const role = await channel.guild.roles.cache.get(pingRoleForMinigames);

    const messageContent = `**It's time for Russian roulette! React to this message to participate and win 8 botcoins!** ${role.toString()}`;

    const ruletaEmbed = {
        title: 'Russian roulette',
        color: 0xff8457,
        description: 'Participate now by reacting to this message!',
    };

    const message = await channel.send({ content: messageContent, embeds: [ruletaEmbed] });
    await message.react('🔫');

    await new Promise(resolve => setTimeout(resolve, 130000));

    const reactionMessage = await channel.messages.fetch(message.id);
    const participants = await reactionMessage.reactions.cache.get('🔫').users.fetch();
    const realParticipants = participants.filter(user => !user.bot && user.id !== client.user.id);

    if (realParticipants.size > 1) {
        let interval = null;
        let eliminatedPlayers = new Set();
        const startGame = async () => {
            interval = setInterval(async () => {
                const reactionMessage = await channel.messages.fetch(message.id);
                const participants = await reactionMessage.reactions.cache.get('🔫').users.fetch();
                const realParticipants = participants.filter(user => !eliminatedPlayers.has(user) && !user.bot && user.id !== client.user.id);

                if (realParticipants.size === 1) {
                    clearInterval(interval);
                    const winner = realParticipants.first();
                    const user_id = winner.id;

                    if (!tradeCounts[user_id]) {
                        const winnerNoRegisterEmbed = {
                            title: 'Russian roulette winner',
                            color: 0xf2f290,
                            description: `${winner.toString()}, you survived the Russian roulette but you are not registered. Register to enjoy all the bot features`,
                        };
                        await channel.send({ embeds: [winnerNoRegisterEmbed] });
                    } else {
                        tradeCounts[user_id].botcoins += 8;
                        saveTradeLog(tradeCounts);
                        const winnerRegisteredEmbed = {
                            title: 'Russian roulette winner',
                            color: 0xf2f290,
                            description: `${winner.toString()}, you survived the russian roulette and won **8** botcoins. You now have **${tradeCounts[user_id].botcoins}** botcoins`,
                        };
                        await channel.send({ embeds: [winnerRegisteredEmbed] });
                    }

                    setTimeout(selectMiniGame, 900000);
                } else if (realParticipants.size > 1) {
                    const remainingParticipants = realParticipants.filter(user => !eliminatedPlayers.has(user));
                    if (remainingParticipants.size > 1) {
                        const eliminated = remainingParticipants.random();
                        eliminatedPlayers.add(eliminated);
                        const eliminatedEmbed = {
                            title: 'Player eliminated',
                            color: 0xD32F2F,
                            description: `${eliminated.toString()} has died`,
                        };
                        await channel.send({ embeds: [eliminatedEmbed] });
                    }
                } else {
                    clearInterval(interval);
                    const noParticipantsEmbed = {
                        title: 'Game end',
                        color: 0xD32F2F,
                        description: 'There are not enough participants to play russian roulette',
                    };
                    await channel.send({ embeds: [noParticipantsEmbed] });
                    setTimeout(selectMiniGame, 900000);
                }
            }, 10000);
        };

        startGame();
    } else {
        const noParticipantsEmbed = {
            title: 'Game end',
            color: 0xD32F2F,
            description: 'Not enough players to start the game',
        };
        await channel.send({ embeds: [noParticipantsEmbed] });
        setTimeout(selectMiniGame, 900000);
    }
}


async function numberGuessingGame() {
    const channel = await client.channels.fetch(minigamesChannel);
    const role = await channel.guild.roles.cache.get(pingRoleForMinigames);

    const numberToGuess = Math.floor(Math.random() * 100) + 1;
    const maxAttempts = 3;

    const messageContent = `**It's time for the number guessing game! Guess the number between 1 and 100 to win 9 botcoins!** ${role.toString()}`;

    const gameEmbed = {
        title: 'Number guessing game',
        color: 0xff8457,
        description: `The game has started. Write a number between 1 and 100 to guess the secret number!`,
        fields: [
            { name: 'Attempts remaining', value: maxAttempts.toString(), inline: false }
        ]
    };

    const message = await channel.send({ content: messageContent, embeds: [gameEmbed] });

    const thread = await message.startThread({
        name: 'Number guessing',
        autoArchiveDuration: 60
    });

    await thread.send('The game has started. Write a number between 1 and 100 to guess the secret number!');

    const playerAttempts = {};

    const filter = m => !m.author.bot;

    const collector = thread.createMessageCollector({ filter, time: 120000 });

    collector.on('collect', async (m) => {
        if (Number.isInteger(parseInt(m.content)) && parseInt(m.content) > 0 && parseInt(m.content) <= 100) {
            const guess = parseInt(m.content);

            if (!tradeCounts[m.author.id]) {
                await thread.send(`${m.author.toString()}, you need to register to participate in the number guessing game`);
                return;
            }

            if (!playerAttempts[m.author.id]) {
                playerAttempts[m.author.id] = maxAttempts;
            }

            if (playerAttempts[m.author.id] === 0) {
                await thread.send(`${m.author.toString()}, you have already used all your attempts and cannot participate further`);
                return;
            }

            playerAttempts[m.author.id]--;

            if (guess === numberToGuess) {
                collector.stop('winner');
                return;
            } else if (guess < numberToGuess) {
                await thread.send(`${m.author.toString()}, the number is **greater than ${guess}** / El numero es **mayor que ${guess}**. Remaining attempts: **${playerAttempts[m.author.id]}**`);
            } else {
                await thread.send(`${m.author.toString()}, the number is **less than ${guess}** / El numero es **menor que ${guess}**. Remaining attempts: **${playerAttempts[m.author.id]}**`);
            }

            if (playerAttempts[m.author.id] === 0) {
                await thread.send(`${m.author.toString()}, you have used all your attempts and cannot participate further`);
            }
        } else {
            await thread.send(`${m.author.toString()}, please enter a valid number between 1 and 100`);
        }
    });

    collector.on('end', async (collected, reason) => {
        await thread.setArchived(true);

        if (reason === 'winner') {
            const winner = collected.last().author;
            tradeCounts[winner.id].botcoins += 9;
            saveTradeLog(tradeCounts);

            const winnerEmbed = {
                title: 'Number guessing',
                color: 0xf2f290,
                description: `${winner.toString()}, you guessed the number and won **9** botcoins. You now have **${tradeCounts[winner.id].botcoins}** botcoins`,
            };
            await channel.send({ embeds: [winnerEmbed] });
        } else {
            const loseEmbed = {
                title: 'Game end',
                color: 0xD32F2F,
                description: `The game is over. The secret number was: **${numberToGuess}**`,
            };
            await channel.send({ embeds: [loseEmbed] });
        }

        setTimeout(() => thread.delete(), 5000);

        setTimeout(selectMiniGame, 900000);
    });
}

async function flagGuessingGame() {
    const channel = await client.channels.fetch(minigamesChannel);
    const role = await channel.guild.roles.cache.get(pingRoleForMinigames);

    const response = await fetch('https://restcountries.com/v3.1/all');
    const countries = await response.json();
    const country = countries[Math.floor(Math.random() * countries.length)];
    const flagUrl = country.flags.png;
    const correctAnswerEnglish = country.name.common.toLowerCase();

    const translations = country.translations || {};
    const correctAnswerSpanish = (translations.spa?.common || correctAnswerEnglish).toLowerCase();

    const maxAttempts = 3;

    const messageContent = `**It's time for the flag guessing game! Guess the country from the flag to win 11 botcoins!** ${role.toString()}`;

    const gameEmbed = {
        title: 'Flag guessing game',
        color: 0xff8457,
        description: `The game has started. Guess the country for the flag below!`,
        image: { url: flagUrl },
        fields: [
            { name: 'Attempts remaining', value: maxAttempts.toString(), inline: false }
        ]
    };

    const message = await channel.send({ content: messageContent, embeds: [gameEmbed] });

    const thread = await message.startThread({
        name: 'Flag guessing',
        autoArchiveDuration: 60
    });

    await thread.send('The game has started. Guess the country for the flag!');

    const playerAttempts = {};

    const filter = m => !m.author.bot;

    const collector = thread.createMessageCollector({ filter, time: 120000 });

    collector.on('collect', async (m) => {
        const guess = m.content.toLowerCase();

        if (!tradeCounts[m.author.id]) {
            await thread.send(`${m.author.toString()}, you need to register to participate in the flag guessing game`);
            return;
        }

        if (!playerAttempts[m.author.id]) {
            playerAttempts[m.author.id] = maxAttempts;
        }

        if (playerAttempts[m.author.id] === 0) {
            await thread.send(`${m.author.toString()}, you have already used all your attempts`);
            return;
        }

        playerAttempts[m.author.id]--;

        if (guess === correctAnswerEnglish || guess === correctAnswerSpanish) {
            collector.stop('winner');
            return;
        } else {
            await thread.send(`${m.author.toString()}, that's incorrect. Remaining attempts: **${playerAttempts[m.author.id]}**`);
        }

        if (playerAttempts[m.author.id] === 0) {
            await thread.send(`${m.author.toString()}, you have used all your attempts`);
        }
    });

    collector.on('end', async (collected, reason) => {
        await thread.setArchived(true);

        if (reason === 'winner') {
            const winner = collected.last().author;
            tradeCounts[winner.id].botcoins += 11;
            saveTradeLog(tradeCounts);

            const winnerEmbed = {
                title: 'Flag guessing',
                color: 0xf2f290,
                description: `${winner.toString()}, you guessed the country and won **11** botcoins. You now have **${tradeCounts[winner.id].botcoins}** botcoins`,
            };
            await channel.send({ embeds: [winnerEmbed] });
        } else {
            const loseEmbed = {
                title: 'Game end',
                color: 0xD32F2F,
                description: `The game is over. The correct country was: **${country.name.common}**`,
            };
            await channel.send({ embeds: [loseEmbed] });
        }

        setTimeout(() => thread.delete(), 5000);

        setTimeout(selectMiniGame, 900000);
    });
}



async function treasureHunt() {
    const channel = await client.channels.fetch(minigamesChannel);
    const role = await channel.guild.roles.cache.get(pingRoleForMinigames);

    const messageContent = `**It's time for a treasure hunting adventure! React to this message to participate and win 9 botcoins!** ${role.toString()}`;

    const treasureEmbed = {
        title: 'Treasure hunt',
        color: 0xff8457,
        description: 'Participate now by reacting to this message!',
    };

    const message = await channel.send({ content: messageContent, embeds: [treasureEmbed] });
    await message.react('🗺️');

    await new Promise(resolve => setTimeout(resolve, 130000));

    const reactionMessage = await channel.messages.fetch(message.id);
    const participants = await reactionMessage.reactions.cache.get('🗺️').users.fetch();
    const realParticipants = participants.filter(user => !user.bot && user.id !== client.user.id);

    if (realParticipants.size > 1) {
        let interval = null;
        let eliminatedPlayers = new Set();
        const deathReasons = [
            "fell into a bottomless pit",
            "was devoured by a tiger",
            "was lost in a sand storm",
            "was bitten by a poisonous snake",
            "got stuck in quicksand",
            "was captured by a cannibalistic tribe",
            "fell off a cliff",
            "was crushed by a giant rock",
            "drowned while crossing a river",
            "was hit by a trap arrow"
        ];

        const startGame = async () => {
            interval = setInterval(async () => {
                const reactionMessage = await channel.messages.fetch(message.id);
                const participants = await reactionMessage.reactions.cache.get('🗺️').users.fetch();
                const realParticipants = participants.filter(user => !eliminatedPlayers.has(user) && !user.bot && user.id !== client.user.id);

                if (realParticipants.size === 1) {
                    clearInterval(interval);
                    const winner = realParticipants.first();
                    const user_id = winner.id;

                    if (!tradeCounts[user_id]) {
                        const winnerNoRegisterEmbed = {
                            title: 'Treasure found!',
                            color: 0xf2f290,
                            description: `<@${user_id}>, you have found the treasure but you are not registered. Register to enjoy all the bot's features`,
                        };
                        await channel.send({ embeds: [winnerNoRegisterEmbed] });
                    } else {
                        tradeCounts[user_id].botcoins += 9;
                        saveTradeLog(tradeCounts);
                        const winnerRegisteredEmbed = {
                            title: 'Treasure found!',
                            color: 0xf2f290,
                            description: `<@${user_id}>, you have found the treasure and earned **9** botcoins. Now you have **${tradeCounts[user_id].botcoins}** botcoins`,
                        };
                        await channel.send({ embeds: [winnerRegisteredEmbed] });
                    }

                    setTimeout(selectMiniGame, 900000);
                } else if (realParticipants.size > 1) {
                    const remainingParticipants = realParticipants.filter(user => !eliminatedPlayers.has(user));
                    if (remainingParticipants.size > 1) {
                        const eliminated = remainingParticipants.random();
                        eliminatedPlayers.add(eliminated);
                        const deathReason = deathReasons[Math.floor(Math.random() * deathReasons.length)];
                        const eliminatedEmbed = {
                            title: 'Adventurer eliminated',
                            color: 0xD32F2F,
                            description: `<@${eliminated.id}> ${deathReason} during treasure hunt`,
                        };
                        await channel.send({ embeds: [eliminatedEmbed] });
                    }
                } else {
                    clearInterval(interval);
                    const noParticipantEmbed = {
                        title: 'Game end',
                        color: 0xD32F2F,
                        description: 'There are not enough participants to play treasure hunt',
                    };
                    await channel.send({ embeds: [noParticipantEmbed] });
                    setTimeout(selectMiniGame, 900000);
                }
            }, 10000);
        };

        startGame();
    } else {
        const noParticipantsEmbed = {
            title: 'Game end',
            color: 0xD32F2F,
            description: 'Not enough players to start the game',
        };
        await channel.send({ embeds: [noParticipantsEmbed] });
        setTimeout(selectMiniGame, 900000);
    }
}
const maxBetsPerHour = 6;
const betCooldownMs = 60 * 60 * 1000;
let betLimits = {};

function loadBetLimits() {
    try {
        const data = fs.readFileSync('betLimits.json', 'utf8');
        betLimits = JSON.parse(data);
    } catch (err) {
        betLimits = {};
    }
}

function saveBetLimits() {
    try {
        fs.writeFileSync('betLimits.json', JSON.stringify(betLimits, null, 2));
    } catch (err) {
        return;
    }
}

function canUserBet(userId) {
    const now = Date.now();
    if (!betLimits[userId]) {
        betLimits[userId] = { bets: [], lastReset: now };
    }

    if (now - betLimits[userId].lastReset > betCooldownMs) {
        betLimits[userId].bets = [];
        betLimits[userId].lastReset = now;
    }

    betLimits[userId].bets = betLimits[userId].bets.filter(bet => now - bet < betCooldownMs);

    return betLimits[userId].bets.length < maxBetsPerHour;
}

function recordBet(userId) {
    if (!betLimits[userId]) {
        betLimits[userId] = { bets: [], lastReset: Date.now() };
    }
    betLimits[userId].bets.push(Date.now());
    saveBetLimits();
}


async function headsOrTails(interaction) {
    const userId = interaction.user.id;
    const userData = tradeCounts[userId];

    loadBetLimits();

    if (!canUserBet(userId)) {
        const betLimitEmbed = {
            embeds: [{
                title: 'Bet limit reached',
                description: `You have reached the limit of **${maxBetsPerHour}** bets per hour. Please try again later`,
                color: 0xD32F2F
            }]
        };
        await interaction.reply(betLimitEmbed);
        return;
    }

    if (!userData || typeof userData !== 'object' || !userData.code) {
        const registerEmbed = {
            title: 'Registration required',
            color: 0xD32F2F,
            description: 'You must register first using **/smoq register**',
        };
        await interaction.reply({ embeds: [registerEmbed] });
        return;
    }

    const amount = interaction.options.getInteger('amount');
    const choice = interaction.options.getString('choice');

    if (userData.botcoins < amount) {
        const botcoinsInsufficientEmbed = {
            title: 'Insufficient botcoins',
            color: 0xD32F2F,
            description: 'You do not have enough available botcoins',
        };
        await interaction.reply({ embeds: [botcoinsInsufficientEmbed] });
        return;
    }

    recordBet(userId);

    const result = Math.random() < 0.5 ? 'heads' : 'tails';

    if (result === choice) {
        userData.botcoins += amount;
        saveTradeLog(tradeCounts);
        const winEmbed = {
            title: 'Favorable wind!',
            color: 0x00AE86,
            description: `Congratulations! You have won **${amount}** botcoins. You now have **${userData.botcoins}** available botcoins`,
            footer: { text: `The result was ${result}` }
        };
        await interaction.reply({ embeds: [winEmbed] });
    } else {
        userData.botcoins -= amount;
        saveTradeLog(tradeCounts);
        const loseEmbed = {
            title: 'Bad luck...',
            color: 0xD32F2F,
            description: `But what a bad luck, you lost **${amount}** botcoins. You now have **${userData.botcoins}** available botcoins`,
            footer: { text: `The result was ${result}` }
        };
        await interaction.reply({ embeds: [loseEmbed] });
    }

    saveBetLimits();
}


async function dice(interaction) {
    const userId = interaction.user.id;
    const userData = tradeCounts[userId];

    loadBetLimits();

    if (!canUserBet(userId)) {
        const betLimitEmbed = {
            embeds: [{
                title: 'Bet limit reached',
                description: `You have reached the limit of **${maxBetsPerHour}** bets per hour. Please try again later`,
                color: 0xD32F2F
            }]
        };
        await interaction.reply(betLimitEmbed);
        return;
    }

    if (!userData || typeof userData !== 'object' || !userData.code) {
        const registerEmbed = {
            title: 'Registration required',
            color: 0xD32F2F,
            description: 'You must register first using **/smoq register**',
        };
        await interaction.reply({ embeds: [registerEmbed] });
        return;
    }

    let cantidad = interaction.options.getInteger('amount');
    let number = interaction.options.getInteger('number');

    if (isNaN(cantidad) || cantidad <= 0) {
        cantidad = 1;
    }

    if (isNaN(number) || number < 1 || number > 6) {
        const invalidNumberEmbed = {
            title: 'Invalid number',
            color: 0xD32F2F,
            description: 'The bet number must be between 1 and 6',
        };
        await interaction.reply({ embeds: [invalidNumberEmbed] });
        return;
    }

    if (userData.botcoins < cantidad) {
        const botcoinsInsufficientEmbed = {
            title: 'Insufficient botcoins',
            color: 0xD32F2F,
            description: 'You do not have enough botcoins available',
        };
        await interaction.reply({ embeds: [botcoinsInsufficientEmbed] });
        return;
    }

    recordBet(userId);

    const result = Math.floor(Math.random() * 6) + 1;

    let resultDescription = `The dice landed on number ${result}`;

    if (result === number) {
        userData.botcoins += cantidad * 3;
        saveTradeLog(tradeCounts);
        const winEmbed = {
            title: 'Favorable wind!',
            color: 0x00AE86,
            description: `Congratulations! You have won **${cantidad * 3}** botcoins. You now have **${userData.botcoins}** botcoins available`,
            footer: { text: resultDescription }
        };
        await interaction.reply({ embeds: [winEmbed] });
    } else {
        userData.botcoins -= cantidad;
        saveTradeLog(tradeCounts);
        const loseEmbed = {
            title: 'Bad luck...',
            color: 0xD32F2F,
            description: `But what a bad luck, you lost **${cantidad}** botcoins. You now have **${userData.botcoins}** botcoins available`,
            footer: { text: resultDescription }
        };
        await interaction.reply({ embeds: [loseEmbed] });
    }

    saveBetLimits();
}


async function colorRoulette(interaction) {
    const userId = interaction.user.id;
    const userData = tradeCounts[userId];

    loadBetLimits();

    if (!canUserBet(userId)) {
        const betLimitEmbed = {
            embeds: [{
                title: 'Bet limit reached',
                description: `You have reached the limit of **${maxBetsPerHour}** bets per hour. Please try again later`,
                color: 0xD32F2F
            }]
        };
        await interaction.reply(betLimitEmbed);
        return;
    }

    if (!userData || typeof userData !== 'object' || !userData.code) {
        const registerEmbed = {
            title: 'Registration required',
            color: 0xD32F2F,
            description: 'You must register first using **/smoq register**',
        };
        await interaction.reply({ embeds: [registerEmbed] });
        return;
    }

    const amount = interaction.options.getInteger('amount');
    const chosenColor = interaction.options.getString('color').toLowerCase();

    if (userData.botcoins < amount) {
        const botcoinsInsufficientEmbed = {
            title: 'Insufficient botcoins',
            color: 0xD32F2F,
            description: 'You do not have enough botcoins available',
        };
        await interaction.reply({ embeds: [botcoinsInsufficientEmbed] });
        return;
    }

    recordBet(userId);

    const colors = ['red', 'green', 'blue'];
    const winningColor = colors[Math.floor(Math.random() * colors.length)];
    const highlightedWinningColor = `${winningColor}`;

    if (winningColor === chosenColor) {
        userData.botcoins += amount * 2;
        saveTradeLog(tradeCounts);
        const winEmbed = {
            title: 'Favorable wind!',
            color: 0x00AE86,
            description: `Congratulations! You have won **${amount * 2}** botcoins. You now have **${userData.botcoins}** botcoins available`,
            footer: {
                text: `The color on which the roulette landed was ${highlightedWinningColor}`,
            },
        };
        await interaction.reply({ embeds: [winEmbed] });
    } else {
        userData.botcoins -= amount;
        saveTradeLog(tradeCounts);
        const loseEmbed = {
            title: 'Bad luck...',
            color: 0xD32F2F,
            description: `But what a bad luck, you lost **${amount}** botcoins. You now have **${userData.botcoins}** botcoins available`,
            footer: {
                text: `The color on which the roulette landed was ${highlightedWinningColor}`,
            },
        };
        await interaction.reply({ embeds: [loseEmbed] });
    }

    saveBetLimits();
}

async function fishingMG(interaction) {
    const userId = interaction.user.id;
    const userData = tradeCounts[userId];
    if (!userData || typeof userData !== 'object' || !userData.code) {
        const registerEmbed = {
            title: 'Registration required',
            color: 0xD32F2F,
            description: 'You must register first using **/smoq register**',
        };
        await interaction.reply({ embeds: [registerEmbed] });
        return;
    }

    const fishingCost = 15;

    if (userData.botcoins < fishingCost) {
        const botcoinsInsufficientEmbed = {
            title: 'Insufficient botcoins',
            color: 0xD32F2F,
            description: `You do not have enough botcoins available. **${fishingCost}** botcoins are required to fish`,
        };
        await interaction.reply({ embeds: [botcoinsInsufficientEmbed] });
        return;
    }

    userData.botcoins -= fishingCost;
    saveTradeLog(tradeCounts);

    const fishingEmbed = {
        title: 'Fishing...',
        color: 0x00AE86,
        description: 'Fishing has begun. Please wait a few minutes while you try to catch something',
    };

    const message = await interaction.reply({ embeds: [fishingEmbed], fetchReply: true });

    await new Promise((resolve) => setTimeout(resolve, 120000));

    const rewards = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25];
    const reward = rewards[Math.floor(Math.random() * rewards.length)];

    let description;
    if (reward === 0) {
        description = 'Unfortunately, you caught nothing this time.';
    } else {
        userData.botcoins += reward;
        saveTradeLog(tradeCounts);
        description = `Congratulations! You caught **${reward}** botcoins. You now have **${userData.botcoins}** botcoins available`;
    }

    const embed = {
        title: 'Fishing result',
        color: reward > 0 ? 0x00AE86 : 0xD32F2F,
        description: description,
    };

    await message.edit({ embeds: [embed] });
}

async function adminPay(interaction) {
    if (!hasBotPerms(interaction.member)) {
        const noPermsEmbed = {
            title: 'Access denied',
            color: 0xD32F2F,
            description: 'You need bot perms to use this command',
        };
        await interaction.reply({ embeds: [noPermsEmbed] });
        return;
    }

    const targetUser = interaction.options.getUser('user');
    const type = interaction.options.getString('type');
    const amount = interaction.options.getInteger('amount');
    const time = interaction.options.getString('time');

    if (!targetUser) {
        const invalidUserEmbed = {
            title: 'Invalid user',
            color: 0xD32F2F,
            description: 'Could not find the specified user',
        };
        await interaction.reply({ embeds: [invalidUserEmbed] });
        return;
    }

    function calculateExpirationDate(timeString) {
        if (!timeString) return null;

        const now = new Date();
        const [value, unit] = timeString.toLowerCase().split(' ');
        const numValue = parseInt(value);

        switch (unit) {
            case 'day':
            case 'days':
                now.setDate(now.getDate() + numValue);
                break;
            case 'week':
            case 'weeks':
                now.setDate(now.getDate() + (numValue * 7));
                break;
            case 'month':
            case 'months':
                now.setMonth(now.getMonth() + numValue);
                break;
            case 'year':
            case 'years':
                now.setFullYear(now.getFullYear() + numValue);
                break;
            default:
                return null;
        }

        return Math.floor(now.getTime());
    }

    const targetUserId = targetUser.id;

    if (!tradeCounts[targetUserId]) {
        tradeCounts[targetUserId] = { trades_remaining: 0, botcoins: 0 };
    }

    if (amount !== null) {
        const expirationDate = calculateExpirationDate(time);

        if (type === 'trades' || type === 'both') {
            tradeCounts[targetUserId].trades_remaining = (tradeCounts[targetUserId].trades_remaining || 0) + amount;
        }
        if (type === 'botcoins' || type === 'both') {
            tradeCounts[targetUserId].botcoins = (tradeCounts[targetUserId].botcoins || 0) + amount;
        }
        if (expirationDate) {
            tradeCounts[targetUserId].expiration_date = expirationDate;
        }

        saveTradeLog(tradeCounts);

        const typeDescription = type === 'both' ? 'trades and botcoins' : type;
        const timeDescription = time ? ` (expires in ${time})` : '';
        const successEmbed = {
            title: 'Success',
            color: 0x00AE86,
            description: `${targetUser} has been given **${amount}** ${typeDescription}${timeDescription}`,
        };

        await interaction.reply({ embeds: [successEmbed] });
        return;
    }

    const errorEmbed = {
        title: 'Invalid option',
        color: 0xD32F2F,
        description: 'Please provide a valid amount',
    };
    await interaction.reply({ embeds: [errorEmbed] });
}

async function botPermsAdminPay(interaction) {
    if (!hasBotPerms(interaction.member)) {
        const noPermsEmbed = {
            title: 'Access denied',
            color: 0xD32F2F,
            description: 'You need bot perms to use this command',
        };
        await interaction.reply({ embeds: [noPermsEmbed] });
        return;
    }

    const targetUser = interaction.options.getUser('user');
    const type = interaction.options.getString('type');
    const amount = interaction.options.getInteger('amount');

    if (!targetUser) {
        const invalidUserEmbed = {
            title: 'Invalid user',
            color: 0xD32F2F,
            description: 'Could not find the specified user',
        };
        await interaction.reply({ embeds: [invalidUserEmbed] });
        return;
    }

    const targetUserId = targetUser.id;

    if (!tradeCounts[targetUserId]) {
        tradeCounts[targetUserId] = { trades_remaining: 0, botcoins: 0 };
    }

    if (amount !== null) {
        if (type === 'trades' || type === 'both') {
            tradeCounts[targetUserId].trades_remaining = (tradeCounts[targetUserId].trades_remaining || 0) + amount;
        }
        if (type === 'botcoins' || type === 'both') {
            tradeCounts[targetUserId].botcoins = (tradeCounts[targetUserId].botcoins || 0) + amount;
        }

        saveTradeLog(tradeCounts);

        const typeDescription = type === 'both' ? 'trades and botcoins' : type;
        const successEmbed = {
            title: 'Success',
            color: 0x00AE86,
            description: `${targetUser} has been given **${amount}** ${typeDescription}`,
        };

        await interaction.reply({ embeds: [successEmbed] });
        return;
    }

    const errorEmbed = {
        title: 'Invalid option',
        color: 0xD32F2F,
        description: 'Please provide a valid amount',
    };
    await interaction.reply({ embeds: [errorEmbed] });
}

function checkExpirationDates() {
    const currentDate = Date.now();

    for (const userId in tradeCounts) {
        const userData = tradeCounts[userId];
        if (userData.expiration_date && userData.expiration_date <= currentDate) {
            userData.trades_remaining = 0;
            userData.botcoins = 0;
            delete userData.expiration_date;
        }
    }

    saveTradeLog(tradeCounts);
}

async function adminRemoveTrades(interaction) {

    if (!hasBotPerms(interaction.member)) {
        const noPermsEmbed = {
            title: 'Access denied',
            color: 0xD32F2F,
            description: 'You need bot perms to use this command',
        };
        await interaction.reply({ embeds: [noPermsEmbed] });
        return;
    }

    const targetUser = interaction.options.getUser('user');
    const amount = interaction.options.getString('amount');
    const type = interaction.options.getString('type');

    if (!targetUser) {
        const noTargetUserEmbed = {
            title: 'Invalid user',
            color: 0xD32F2F,
            description: 'You need to mention a user to use this function',
        };
        await interaction.reply({ embeds: [noTargetUserEmbed] });
        return;
    }

    const targetUserData = tradeCounts[targetUser.id];

    if (!targetUserData) {
        const userNotRegisteredEmbed = {
            title: 'User not registered',
            color: 0xD32F2F,
            description: 'The user you are trying to modify is not registered',
        };
        await interaction.reply({ embeds: [userNotRegisteredEmbed] });
        return;
    }

    if (amount.toLowerCase() === "all") {
        if (type === 'trades') {
            targetUserData.trades_remaining = 0;
        } else if (type === 'botcoins') {
            targetUserData.botcoins = 0;
        } else if (type === 'both') {
            targetUserData.trades_remaining = 0;
            targetUserData.botcoins = 0;
        } else {
            const invalidTypeEmbed = {
                title: 'Invalid type',
                color: 0xD32F2F,
                description: 'The type must be "trades", "botcoins", or "both"',
            };
            await interaction.reply({ embeds: [invalidTypeEmbed] });
            return;
        }

        saveTradeLog(tradeCounts);

        const successEmbed = {
            title: 'Success',
            color: 0x00AE86,
            description: `All ${type} for <@${targetUser.id}> have been removed successfully`,
        };

        await interaction.reply({ embeds: [successEmbed] });
    } else {
        const amountInt = parseInt(amount, 10);
        if (isNaN(amountInt) || amountInt <= 0) {
            const invalidAmountEmbed = {
                title: 'Invalid amount',
                color: 0xD32F2F,
                description: 'The amount must be a positive integer or "all"',
            };
            await interaction.reply({ embeds: [invalidAmountEmbed] });
            return;
        }

        if (type === 'trades') {
            targetUserData.trades_remaining = Math.max(targetUserData.trades_remaining - amountInt, 0);
        } else if (type === 'botcoins') {
            targetUserData.botcoins = Math.max(targetUserData.botcoins - amountInt, 0);
        } else if (type === 'both') {
            targetUserData.trades_remaining = Math.max(targetUserData.trades_remaining - amountInt, 0);
            targetUserData.botcoins = Math.max(targetUserData.botcoins - amountInt, 0);
        } else {
            const invalidTypeEmbed = {
                title: 'Invalid type',
                color: 0xD32F2F,
                description: 'The type must be "trades", "botcoins", or "both"',
            };
            await interaction.reply({ embeds: [invalidTypeEmbed] });
            return;
        }

        saveTradeLog(tradeCounts);

        const successEmbed = {
            title: 'Success',
            color: 0x00AE86,
            description: `**${amountInt}** ${type} for <@${targetUser.id}> have been removed successfully`,
        };

        await interaction.reply({ embeds: [successEmbed] });
    }
}

function generateRandomCode(characters) {
    let result = '';
    for (let i = 0; i < 6; i++) {
        const randomIndex = Math.floor(Math.random() * characters.length);
        result += characters[randomIndex];
    }
    return result;
}

const regaladonInProgress = new Map();

async function regaladonAdmin(interaction) {
    if (!hasBotPerms(interaction.member)) {
        const noPermsEmbed = {
            title: 'Access denied',
            color: 0xD32F2F,
            description: 'You need bot perms to use this command',
        };
        await interaction.reply({ embeds: [noPermsEmbed] });
        return;
    }

    const userId = interaction.user.id;

    if (regaladonInProgress.get(userId)) {
        const busyEmbed = {
            title: 'Process in progress',
            color: 0xD32F2F,
            description: 'You already have an open invite in progress. Please wait for it to complete',
        };
        await interaction.reply({ embeds: [busyEmbed] });
        return;
    }

    const timeInMinutes = interaction.options.getInteger('minutes');

    if (!timeInMinutes || timeInMinutes <= 0 || timeInMinutes > 10) {
        const errorEmbed = {
            title: 'Error in the time value',
            color: 0xD32F2F,
            description: 'Please specify a valid number of minutes (1-10)',
        };
        await interaction.reply({ embeds: [errorEmbed] });
        return;
    }

    regaladonInProgress.set(userId, true);

    const characters = 'BCDFGHKLMNPQRSTVWX23456789';
    const randomCode = generateRandomCode(characters);
    const timeInSeconds = timeInMinutes * 60;

    const successEmbed = {
        title: 'Open invite in process!',
        color: 0x00AE86,
        description: `Open invite is in process! Will be active for **${timeInMinutes}** minutes\nBot code is **${randomCode}**`,
    };
    const reply = await interaction.reply({ embeds: [successEmbed], fetchReply: true });

    try {
        const pythonProcess = spawn('python3', ['rgbt-25.py', 'tiempo', timeInSeconds.toString(), randomCode]);

        await new Promise((resolve, reject) => {
            pythonProcess.stdout.on('data', (data) => {
                console.log(`stdout: ${data}`);
            });

            pythonProcess.stderr.on('data', (data) => {
                console.error(`stderr: ${data}`);
            });

            pythonProcess.on('close', async (code) => {
                if (code === 0) {
                    const completedEmbed = {
                        title: 'Success!',
                        color: 0x00AE86,
                        description: `The bot code was successful!`,
                    };
                    await interaction.editReply({ embeds: [completedEmbed] });
                } else {
                    const errorEmbed = {
                        title: 'Error',
                        color: 0xD32F2F,
                        description: 'There was an error processing the bot code. Please try again',
                    };
                    await interaction.editReply({ embeds: [errorEmbed] });
                }
                resolve();
            });

            pythonProcess.on('error', (error) => {
                reject(error);
            });
        });
    } catch (error) {
        const errorEmbed = {
            title: 'Error',
            color: 0xD32F2F,
            description: 'An unexpected error occurred. Please try again',
        };
        await interaction.editReply({ embeds: [errorEmbed] });
    } finally {
        regaladonInProgress.delete(userId);
    }
}

const slotSymbols = ['🍒', '🍋', '🍊', '🍇', '🍓', '💎', '🔔', '💰', '⭐', '👻', '🎃', '🌈', '🌟', '🍀', '🎲'];

async function playSlots(interaction) {
    const userId = interaction.user.id;
    const userData = tradeCounts[userId];

    loadBetLimits();

    if (!canUserBet(userId)) {
        const betLimitEmbed = {
            embeds: [{
                title: 'Bet limit reached',
                description: `You have reached the limit of **${maxBetsPerHour}** bets per hour. Please try again later`,
                color: 0xD32F2F
            }]
        };
        await interaction.reply(betLimitEmbed);
        return;
    }

    if (!userData || typeof userData !== 'object' || !userData.code) {
        const registerEmbed = {
            title: 'Registration required',
            color: 0xD32F2F,
            description: 'You must register first using **/smoq register**',
        };
        await interaction.reply({ embeds: [registerEmbed] });
        return;
    }

    const amount = interaction.options.getInteger('amount');

    if (userData.botcoins < amount) {
        const botcoinsInsufficientEmbed = {
            title: 'Insufficient botcoins',
            color: 0xD32F2F,
            description: 'You do not have enough botcoins available',
        };
        await interaction.reply({ embeds: [botcoinsInsufficientEmbed] });
        return;
    }

    recordBet(userId);

    const startingMachineEmbed = {
        title: 'Starting the machine...',
        color: 0x00AE86,
        description: 'Starting the slots machine!',
    };
    await interaction.reply({ embeds: [startingMachineEmbed] });

    await new Promise(resolve => setTimeout(resolve, 2000));

    const spinEmbed = {
        title: 'Spinning the slots...',
        color: 0xf2f290,
        description: '| 🔄 | 🔄 | 🔄 |',
    };
    const message = await interaction.fetchReply();

    const spinAnimation = async () => {
        const symbols = ['🔄', '🔄', '🔄'];
        for (let i = 0; i < 10; i++) {
            const randomSymbols = slotSymbols.sort(() => Math.random() - 0.5);
            symbols[0] = randomSymbols[0];
            symbols[1] = randomSymbols[1];
            symbols[2] = randomSymbols[2];
            const description = `| ${symbols[0]} | ${symbols[1]} | ${symbols[2]} |`;
            await message.edit({ embeds: [{ ...spinEmbed, description }] });
            await new Promise(resolve => setTimeout(resolve, 200));
        }
    };

    await spinAnimation();

    const results = [];
    for (let i = 0; i < 3; i++) {
        if (Math.random() < 0.8) {
            results.push(slotSymbols[Math.floor(Math.random() * slotSymbols.length)]);
        } else {
            results.push(results[i - 1] || slotSymbols[Math.floor(Math.random() * slotSymbols.length)]);
        }
    }

    let multiplier;
    if (results[0] === results[1] && results[1] === results[2]) {
        multiplier = 3;
    } else if (results[0] === results[1] || results[1] === results[2] || results[0] === results[2]) {
        multiplier = 2;
    } else {
        multiplier = 0;
    }

    const winAmount = amount * multiplier;

    const resultDescription = `| ${results[0]} | ${results[1]} | ${results[2]} |`;

    if (multiplier > 0) {
        userData.botcoins = (userData.botcoins || 0) + winAmount;
        saveTradeLog(tradeCounts);
        const winEmbed = {
            title: 'Favorable wind!',
            color: 0x00AE86,
            description: `${resultDescription}\n\nCongratulations! You have won **${winAmount}** botcoins`,
        };
        await message.edit({ embeds: [winEmbed] });
    } else {
        userData.botcoins = (userData.botcoins || 0) - amount;
        saveTradeLog(tradeCounts);
        const loseEmbed = {
            title: 'Bad luck...',
            color: 0xD32F2F,
            description: `${resultDescription}\n\nUnfortunately, you didn't get any matching symbols. You lost **${amount}** botcoins`,
        };
        await message.edit({ embeds: [loseEmbed] });
    }

    saveBetLimits();
}

const PROMOCODE_FILE = path.join(__dirname, 'promocodes.json');

function loadPromocodes() {
    try {
        const data = fs.readFileSync(PROMOCODE_FILE);
        return JSON.parse(data);
    } catch (error) {
        return {};
    }
}

function savePromocodes(promocodes) {
    fs.writeFileSync(PROMOCODE_FILE, JSON.stringify(promocodes, null, 2));
}
async function addPromocode(interaction) {
    const userId = interaction.user.id;

    if (!isAdmin(userId)) {
        const notAdminEmbed = {
            title: 'Access denied',
            color: 0xD32F2F,
            description: 'You do not have permission to run this command',
        };
        await interaction.reply({ embeds: [notAdminEmbed], ephemeral: true });
        return;
    }

    const botcoins = interaction.options.getInteger('bcoins');
    const duration = interaction.options.getInteger('duration');
    const customCode = interaction.options.getString('code') || null;
    const code = customCode || Math.random().toString(36).substring(2, 8).toUpperCase();
    const expiryTime = Date.now() + duration * 3600000;
    const expiry = `<t:${Math.floor(expiryTime / 1000)}:R>`;

    const successEmbed = {
        title: 'Promocode created',
        color: 0x00AE86,
        description: `A new promocode has been created: **\`${code}\`**\nAwards **${botcoins}** botcoins and expires **${expiry}**`,
    };

    await interaction.reply({ embeds: [successEmbed] });

    const promocodes = loadPromocodes();
    promocodes[code] = {
        botcoins,
        expiryTime,
        claimedBy: []
    };
    savePromocodes(promocodes);
}

function removeExpiredPromocodes() {
    const promocodes = loadPromocodes();
    const currentTime = Date.now();
    let removedCount = 0;

    for (const code in promocodes) {
        if (promocodes[code].expiryTime <= currentTime) {
            delete promocodes[code];
            removedCount++;
        }
    }

    if (removedCount > 0) {
        savePromocodes(promocodes);
    } else {
        return;
    }
}

async function redeemPromocode(interaction) {
    const userId = interaction.user.id;
    const code = interaction.options.getString('promocode');
    const promocodes = loadPromocodes();

    if (!(code in promocodes)) {
        const invalidCodeEmbed = {
            title: 'Invalid code',
            color: 0xD32F2F,
            description: 'The entered code is invalid or has expired',
        };
        await interaction.reply({ embeds: [invalidCodeEmbed] });
        return;
    }

    const promocode = promocodes[code];

    if (new Date() > new Date(promocode.expiry)) {
        const expiredCodeEmbed = {
            title: 'Code expired',
            color: 0xD32F2F,
            description: `The promocode **${code}** has expired`,
        };
        await interaction.reply({ embeds: [expiredCodeEmbed] });
        delete promocodes[code];
        savePromocodes(promocodes);
        return;
    }

    if (promocode.claimedBy.includes(userId)) {
        const alreadyClaimedEmbed = {
            title: 'Already claimed',
            color: 0xD32F2F,
            description: 'You have already claimed this promocode',
        };
        await interaction.reply({ embeds: [alreadyClaimedEmbed] });
        return;
    }

    const userData = tradeCounts[userId];

    if (!userData || typeof userData !== 'object' || !userData.code) {
        const registerEmbed = {
            title: 'Registration required',
            color: 0xD32F2F,
            description: 'You must register first using **/smoq register**',
        };
        await interaction.reply({ embeds: [registerEmbed] });
        return;
    }

    userData.botcoins = (userData.botcoins || 0) + promocode.botcoins;
    saveTradeLog(tradeCounts);

    const successEmbed = {
        title: 'Promocode redeemed',
        color: 0x00AE86,
        description: `You have received **${promocode.botcoins}** botcoins. You now have **${userData.botcoins}** botcoins available`,
    };
    await interaction.reply({ embeds: [successEmbed] });

    promocode.claimedBy.push(userId);
    savePromocodes(promocodes);
}


cron.schedule('0 0 * * *', () => {
    const promocodes = loadPromocodes();
    const now = new Date();
    let updated = false;

    for (const [code, details] of Object.entries(promocodes)) {
        if (new Date(details.expiry) < now) {
            delete promocodes[code];
            updated = true;
        }
    }

    if (updated) {
        savePromocodes(promocodes);
    }
});


async function exchangeBotcoinsForTrades(interaction) {
    const userId = interaction.user.id;
    const botcoinsToExchange = interaction.options.getInteger('amount');
    const userData = tradeCounts[userId];

    if (!userData || typeof userData !== 'object' || !userData.code) {
        const registerEmbed = {
            title: 'Registration required',
            color: 0xD32F2F,
            description: 'You must register first using **/smoq register**',
        };
        await interaction.reply({ embeds: [registerEmbed] });
        return;
    }

    if (botcoinsToExchange < 20) {
        const invalidAmountEmbed = {
            title: 'Invalid amount',
            color: 0xD32F2F,
            description: 'The minimum amount of botcoins to exchange is **20**',
        };
        await interaction.reply({ embeds: [invalidAmountEmbed] });
        return;
    }

    if (userData.botcoins < botcoinsToExchange) {
        const insufficientBotcoinsEmbed = {
            title: 'Insufficient botcoins',
            color: 0xD32F2F,
            description: 'You do not have enough botcoins to make an exchange',
        };
        await interaction.reply({ embeds: [insufficientBotcoinsEmbed] });
        return;
    }

    const tradesReceived = Math.floor(botcoinsToExchange / 20);
    userData.botcoins -= botcoinsToExchange;
    userData.trades_remaining += tradesReceived;
    saveTradeLog(tradeCounts);

    const successEmbed = {
        title: 'Exchange successful',
        color: 0x00AE86,
        description: `You have exchanged **${botcoinsToExchange}** botcoins for **${tradesReceived}** trades. You now have **${userData.botcoins}** botcoins and **${userData.trades_remaining}** available trades`,
    };
    await interaction.reply({ embeds: [successEmbed] });
}


const crashProbability = 0.11;
async function crash(interaction) {
    const userId = interaction.user.id;
    const userData = tradeCounts[userId];

    loadBetLimits();

    if (!canUserBet(userId)) {
        const betLimitEmbed = {
            embeds: [{
                title: 'Bet limit reached',
                description: `You have reached the limit of **${maxBetsPerHour}** bets per hour. Please try again later`,
                color: 0xD32F2F
            }]
        };
        await interaction.reply(betLimitEmbed);
        return;
    }

    if (!userData || typeof userData !== 'object' || !userData.code) {
        const registerRequiredEmbed = {
            embeds: [{
                title: 'Registration required',
                description: 'You must register first using **/smoq register**',
                color: 0xD32F2F
            }]
        };

        await interaction.reply(registerRequiredEmbed);
        return;
    }

    const amount = interaction.options.getInteger('amount');

    if (userData.botcoins < amount) {
        const insufficientBotcoinsEmbed = {
            embeds: [{
                title: 'Insufficient botcoins',
                description: 'You do not have enough botcoins available',
                color: 0xD32F2F
            }]
        };

        await interaction.reply(insufficientBotcoinsEmbed);
        return;
    }

    recordBet(userId);

    let multiplier = 1;
    let cashedOut = false;
    let gameEnded = false;

    const cashOut = async () => {
        if (!cashedOut && !gameEnded) {
            cashedOut = true;
            userData.botcoins += Math.floor(amount * multiplier) - amount;
            saveTradeLog(tradeCounts);
            const cashOutEmbed = {
                embeds: [{
                    title: 'You retired on time!',
                    description: `You have withdrawn your bet with a multiplier of **${multiplier.toFixed(2)}x** and have won **${Math.floor(amount * multiplier - amount)}** botcoins. You now have **${userData.botcoins}** botcoins available`,
                    color: 0x00AE86
                }],
                components: []
            };

            await interaction.editReply(cashOutEmbed);
        }
    };

    const gameStartEmbed = {
        embeds: [{
            title: 'Crash game will start soon!',
            description: `Initial bet: **${amount}** botcoins`,
            color: 0x00AE86
        }]
    };

    await interaction.reply(gameStartEmbed);

    await new Promise(resolve => setTimeout(resolve, 3000));

    const retireButton = new ButtonBuilder()
        .setCustomId('retirar')
        .setLabel('Withdraw')
        .setStyle(ButtonStyle.Primary);

    const row = new ActionRowBuilder().addComponents(retireButton);

    const collector = interaction.channel.createMessageComponentCollector({
        componentType: ComponentType.Button,
        filter: i => i.customId === 'retirar' && i.user.id === userId,
        time: 30000
    });

    const interval = setInterval(async () => {
        if (gameEnded) return;

        if (Math.random() < crashProbability) {
            clearInterval(interval);
            gameEnded = true;
            if (!cashedOut) {
                userData.botcoins -= amount;
                saveTradeLog(tradeCounts);
                const crashEmbed = {
                    embeds: [{
                        title: 'It exploded!',
                        description: `The multiplier reached **${multiplier.toFixed(2)}x** and burst. You have lost your bet of **${amount}** botcoins. You now have **${userData.botcoins}** botcoins available`,
                        color: 0xD32F2F
                    }],
                    components: []
                };

                await interaction.editReply(crashEmbed);
            }
            collector.stop();
        } else {
            multiplier += 0.1;
            await interaction.editReply({
                embeds: [{
                    title: 'The crash minigame is on!',
                    description: `🚀 **Multiplier: ${multiplier.toFixed(2)}x**`,
                    color: 0x7289DA
                }],
                components: [row]
            });
        }
    }, 1000);

    collector.on('collect', async i => {
        if (i.customId === 'retirar') {
            clearInterval(interval);
            await i.deferUpdate();
            await cashOut();
            collector.stop();
        }
    });

    collector.on('end', async () => {
        if (!cashedOut && !gameEnded) {
            gameEnded = true;
            userData.botcoins -= amount;
            saveTradeLog(tradeCounts);
            const timeOutEmbed = {
                embeds: [{
                    title: 'Time out',
                    description: `You have not withdrawn your bet on time. You have lost **${amount}** botcoins. You now have **${userData.botcoins}** botcoins available`,
                    color: 0xD32F2F
                }],
                components: []
            };

            await interaction.editReply(timeOutEmbed);
        }
    });

    saveBetLimits();
}

async function searchDb(interaction) {
    try {
        const pageSize = 10;
        const timeoutDuration = 60000;
        const playerName = interaction.options.getString('name').toLowerCase();

        const filteredPlayers = playersDB.filter(player =>
            player.name.toLowerCase().includes(playerName)
        ).sort((a, b) => b.grl - a.grl);

        if (filteredPlayers.length === 0) {
            return await interaction.reply({
                embeds: [{
                    title: 'No results found',
                    description: `No players found with the name "${playerName}"`,
                    color: 0xD32F2F
                }]
            });
        }

        const state = {
            currentPage: 1,
            totalPages: Math.ceil(filteredPlayers.length / pageSize)
        };

        const createPageEmbed = () => {
            const startIndex = (state.currentPage - 1) * pageSize;
            const pagePlayers = filteredPlayers.slice(startIndex, startIndex + pageSize);

            return {
                title: `Search results: ${playerName}`,
                description: pagePlayers.map((player, index) => (
                    `${startIndex + index + 1}. **${player.name}**\n` +
                    `└ ${player.version} • GRL: ${player.grl} • ID: \`${player.id}\``
                )).join('\n\n'),
                color: 0x00AE86,
                footer: {
                    text: `Page ${state.currentPage}/${state.totalPages} • Total: ${filteredPlayers.length} players`
                }
            };
        };

        const createNavigationButtons = () => {
            return new ActionRowBuilder().addComponents(
                new ButtonBuilder()
                    .setCustomId('first')
                    .setLabel('⏮️')
                    .setStyle(ButtonStyle.Secondary)
                    .setDisabled(state.currentPage === 1),
                new ButtonBuilder()
                    .setCustomId('prev')
                    .setLabel('◀️')
                    .setStyle(ButtonStyle.Primary)
                    .setDisabled(state.currentPage === 1),
                new ButtonBuilder()
                    .setCustomId('next')
                    .setLabel('▶️')
                    .setStyle(ButtonStyle.Primary)
                    .setDisabled(state.currentPage === state.totalPages),
                new ButtonBuilder()
                    .setCustomId('last')
                    .setLabel('⏭️')
                    .setStyle(ButtonStyle.Secondary)
                    .setDisabled(state.currentPage === state.totalPages)
            );
        };

        const updateMessage = async (i) => {
            await i.update({
                embeds: [createPageEmbed()],
                components: state.totalPages > 1 ? [createNavigationButtons()] : []
            });
        };

        const message = await interaction.reply({
            embeds: [createPageEmbed()],
            components: state.totalPages > 1 ? [createNavigationButtons()] : [],
            fetchReply: true
        });

        if (state.totalPages <= 1) return;

        const collector = message.createMessageComponentCollector({
            componentType: ComponentType.Button,
            time: timeoutDuration
        });

        collector.on('collect', async (i) => {
            if (i.user.id !== interaction.user.id) {
                await i.deferUpdate();
                return;
            }

            switch (i.customId) {
                case 'first':
                    state.currentPage = 1;
                    break;
                case 'prev':
                    state.currentPage = Math.max(1, state.currentPage - 1);
                    break;
                case 'next':
                    state.currentPage = Math.min(state.totalPages, state.currentPage + 1);
                    break;
                case 'last':
                    state.currentPage = state.totalPages;
                    break;
            }

            await updateMessage(i);
        });

        collector.on('end', () => {
            const finalButtons = createNavigationButtons();
            finalButtons.components.forEach(button => button.setDisabled(true));

            interaction.editReply({
                embeds: [createPageEmbed()],
                components: [finalButtons]
            }).catch(console.error);
        });

    } catch (error) {
        await interaction.reply({
            embeds: [{
                title: 'Error',
                description: 'An error occurred while processing your search',
                color: 0xD32F2F
            }]
        });
    }
}
const rewardTrades = 50;
const cooldownDays = 2;
const cooldownMs = cooldownDays * 24 * 60 * 60 * 1000;

const claimDataFile = path.join(__dirname, 'claimData.json');

function loadClaimData(callback) {
    fs.readFile(claimDataFile, 'utf8', (err, data) => {
        if (err) {
            if (err.code === 'ENOENT') {
                callback(null, {});
            } else {
                return;
            }
        } else {
            try {
                const parsedData = data ? JSON.parse(data) : {};
                callback(null, parsedData);
            } catch (parseError) {
                return;
            }
        }
    });
}

function saveClaimData(data, callback) {
    fs.writeFile(claimDataFile, JSON.stringify(data, null, 2), 'utf8', err => {
        if (err) {
            callback(err);
        } else {
            callback(null);
        }
    });
}

function hasUserBoosted(interaction, callback) {
    const member = interaction.member;
    callback(null, member.premiumSince !== null);
}

function claimBoosts(interaction) {
    try {
        const user = interaction.user;
        const userId = user.id;

        const userData = tradeCounts[userId];

        if (!userData || typeof userData !== 'object' || !userData.code) {
            const registerRequiredEmbed = {
                title: 'Registration required',
                description: 'You must register first using **/smoq register**',
                color: 0xD32F2F
            };

            interaction.reply({ embeds: [registerRequiredEmbed] });
            return;
        }

        hasUserBoosted(interaction, (err, boosted) => {
            if (err) {
                return;
            }

            if (!boosted) {
                const notBoostedEmbed = {
                    title: 'Boost required',
                    color: 0xD32F2F,
                    description: `You need to boost the server to use this command`,
                };
                return interaction.reply({ embeds: [notBoostedEmbed] });
            }

            loadClaimData((loadErr, claimData) => {
                if (loadErr) {
                    console.error(loadErr);
                }

                const now = Date.now();
                const nextClaimTime = claimData[userId] || 0;

                if (now < nextClaimTime) {
                    const timeRemaining = nextClaimTime - now;
                    const daysRemaining = Math.floor(timeRemaining / (24 * 60 * 60 * 1000));
                    const hoursRemaining = Math.ceil((timeRemaining % (24 * 60 * 60 * 1000)) / (60 * 60 * 1000));

                    let timeDescription = '';
                    if (daysRemaining > 0) {
                        timeDescription += `**${daysRemaining}** day${daysRemaining !== 1 ? 's' : ''}`;
                        if (hoursRemaining > 0) {
                            timeDescription += ` and **${hoursRemaining}** hour${hoursRemaining !== 1 ? 's' : ''}`;
                        }
                    } else {
                        timeDescription = `**${hoursRemaining}** hour${hoursRemaining !== 1 ? 's' : ''}`;
                    }

                    const cooldownEmbed = {
                        title: 'Cooldown active',
                        color: 0xD32F2F,
                        description: `You need to wait ${timeDescription} before claiming trades again!`,
                    };
                    return interaction.reply({ embeds: [cooldownEmbed] });
                }

                tradeCounts[userId].trades_remaining += rewardTrades;

                claimData[userId] = now + cooldownMs;

                saveClaimData(claimData, saveErr => {
                    if (saveErr) {
                        return;
                    }

                    const successEmbed = {
                        title: 'Trades claimed',
                        color: 0x00AE86,
                        description: `You have successfully claimed **${rewardTrades}** trades! Now you have **${tradeCounts[userId].trades_remaining}** trades remaining. You can claim again in ${cooldownDays} days!`,
                    };
                    interaction.reply({ embeds: [successEmbed] }).catch(err => {
                        console.error('Error al enviar la respuesta de éxito:', err);
                    });
                });
            });
        });

    } catch (error) {
        return;
    }
}


async function rockPaperScissors(interaction) {
    const userId = interaction.user.id;
    const userData = tradeCounts[userId];

    loadBetLimits();

    if (!canUserBet(userId)) {
        const betLimitEmbed = {
            embeds: [{
                title: 'Bet limit reached',
                description: `You have reached the limit of **${maxBetsPerHour}** bets per hour. Please try again later`,
                color: 0xD32F2F
            }]
        };
        await interaction.reply(betLimitEmbed);
        return;
    }

    if (!userData || typeof userData !== 'object' || !userData.code) {
        const registerEmbed = {
            title: 'Registration required',
            color: 0xD32F2F,
            description: 'You must register first using **/smoq register**',
        };
        await interaction.reply({ embeds: [registerEmbed] });
        return;
    }

    const bet = interaction.options.getInteger('amount');

    if (userData.botcoins < bet) {
        const insufficientFundsEmbed = {
            title: 'Insufficient botcoins',
            color: 0xD32F2F,
            description: 'You do not have enough botcoins for this bet',
        };
        await interaction.reply({ embeds: [insufficientFundsEmbed] });
        return;
    }

    recordBet(userId);

    const choices = ['rock', 'paper', 'scissors'];
    const emojis = { 'rock': '🪨', 'paper': '📄', 'scissors': '✂️' };
    let userScore = 0;
    let botScore = 0;
    let round = 0;

    const gameEmbed = {
        title: 'Rock paper scissors',
        color: 0x00AE86,
        fields: [
            { name: 'Your score', value: '0', inline: true },
            { name: 'Bot score', value: '0', inline: true },
            { name: 'Round', value: '1/3', inline: true },
        ],
        description: '🔽 Choose your move! 🔽',
    };

    const row = new ActionRowBuilder()
        .addComponents(
            new ButtonBuilder()
                .setCustomId('rock')
                .setLabel('Rock')
                .setEmoji('🪨')
                .setStyle(ButtonStyle.Primary),
            new ButtonBuilder()
                .setCustomId('paper')
                .setLabel('Paper')
                .setEmoji('📄')
                .setStyle(ButtonStyle.Primary),
            new ButtonBuilder()
                .setCustomId('scissors')
                .setLabel('Scissors')
                .setEmoji('✂️')
                .setStyle(ButtonStyle.Primary)
        );

    const message = await interaction.reply({ embeds: [gameEmbed], components: [row], fetchReply: true });

    const filter = i => i.user.id === interaction.user.id && choices.includes(i.customId);
    const collector = message.createMessageComponentCollector({ filter, time: 30000 });

    collector.on('collect', async (i) => {
        await i.deferUpdate();
        const userChoice = i.customId;
        const botChoice = choices[Math.floor(Math.random() * choices.length)];

        let roundResult;
        if (userChoice === botChoice) {
            roundResult = 'Tie!';
        } else if (
            (userChoice === 'rock' && botChoice === 'scissors') ||
            (userChoice === 'paper' && botChoice === 'rock') ||
            (userChoice === 'scissors' && botChoice === 'paper')
        ) {
            userScore++;
            roundResult = 'You win this round!';
        } else {
            botScore++;
            roundResult = 'Bot wins this round!';
        }

        round++;
        gameEmbed.fields[0].value = `${userScore} ${userScore > botScore ? '' : ''}`;
        gameEmbed.fields[1].value = `${botScore} ${botScore > userScore ? '' : ''}`;
        gameEmbed.fields[2].value = `${round}/3`;
        gameEmbed.description = `Round ${round}: You chose ${emojis[userChoice]} - Bot chose ${emojis[botChoice]} - ${roundResult}`;

        if (round === 3 || userScore === 2 || botScore === 2) {
            collector.stop();
        } else {
            await i.editReply({ embeds: [gameEmbed], components: [row] });
        }
    });

    collector.on('end', async () => {
        let finalResult;
        if (userScore > botScore) {
            finalResult = `You win! You've earned **${bet * 2}** botcoins`;
            userData.botcoins += bet;
        } else if (botScore > userScore) {
            finalResult = `Bot wins! You've lost **${bet}** botcoins`;
            userData.botcoins -= bet;
        } else {
            finalResult = "It's a tie! Your bet is returned";
        }

        gameEmbed.description = finalResult;
        gameEmbed.color = userScore > botScore ? 0x00AE86 : botScore > userScore ? 0xD32F2F : 0xf2f290;
        gameEmbed.fields = [
            { name: 'Final score', value: `You: ${userScore} | Bot: ${botScore}`, inline: false },
            { name: 'Your new balance', value: `**${userData.botcoins} botcoins**`, inline: false }
        ];

        saveTradeLog(tradeCounts);
        await interaction.editReply({ embeds: [gameEmbed], components: [] });
    });

    saveBetLimits();
}


async function showDailyGoals(interaction) {
    try {
        const userId = interaction.user.id;
        const userGoals = getUserDailyGoals(userId);
        const userData = tradeCounts[userId];

        if (!userData || typeof userData !== 'object' || !userData.code) {
            const registerEmbed = {
                title: 'Registration required',
                color: 0xD32F2F,
                description: 'You must register first using **/smoq register**',
            };
            await interaction.reply({ embeds: [registerEmbed] });
            return;
        }

        const goalsEmbed = {
            title: 'Daily goals',
            color: 0x00AE86,
            fields: userGoals.goals.map((goal, index) => ({
                name: `Goal ${index + 1}`,
                value: `${goal.description}\nProgress: **${userGoals.progress[index]}/${goal.count}**\nReward: **${goal.reward}** botcoins\nStatus: ${userGoals.completed[index] ? '✅ Completed' : '🔄 In progress'}`
            }))
        };

        await interaction.reply({ embeds: [goalsEmbed] });
    } catch (error) {
        if (!interaction.replied) {
            await interaction.reply({ content: 'Failed to load daily goals', ephemeral: true });
        }
    }
}

const DAILY_GOALS_FILE = path.join(__dirname, 'dailyGoals.json');


const possibleGoals = [
    { type: 'messages', description: 'Send **{count}** messages in the server', minCount: 10, maxCount: 100, reward: { min: 30, max: 60 } },
    { type: 'invites', description: 'Invite **{count}** new users to the server', minCount: 1, maxCount: 5, reward: { min: 50, max: 150 } },
    { type: 'reactions', description: 'React to **{count}** messages', minCount: 5, maxCount: 30, reward: { min: 5, max: 15 } }
];


function loadDailyGoals() {
    try {
        const data = fs.readFileSync(DAILY_GOALS_FILE, 'utf8');
        return JSON.parse(data);
    } catch (error) {
        if (error.code === 'ENOENT') {
            return {};
        }
        return {};
    }
}

function saveDailyGoals(goals) {
    try {
        fs.writeFileSync(DAILY_GOALS_FILE, JSON.stringify(goals, null, 2));
    } catch (error) {
        return;
    }
}

function generateDailyGoals() {
    const today = new Date().toDateString();
    const goals = new Set();

    while (goals.size < 3) {
        const goalIndex = Math.floor(Math.random() * possibleGoals.length);
        const goal = { ...possibleGoals[goalIndex] };

        if (!Array.from(goals).some(g => JSON.parse(g).type === goal.type)) {
            goal.count = Math.floor(Math.random() * (goal.maxCount - goal.minCount + 1)) + goal.minCount;
            goal.reward = Math.floor(Math.random() * (goal.reward.max - goal.reward.min + 1)) + goal.reward.min;
            goal.description = goal.description.replace('{count}', goal.count);
            goals.add(JSON.stringify(goal));
        }
    }

    return Array.from(goals).map(JSON.parse);
}


function getUserDailyGoals(userId) {
    const today = new Date().toDateString();
    const dailyGoals = loadDailyGoals();

    if (!dailyGoals[today]) {
        dailyGoals[today] = {};
        saveDailyGoals(dailyGoals);
    }

    if (!dailyGoals[today][userId]) {
        dailyGoals[today][userId] = {
            goals: generateDailyGoals(),
            progress: Array(3).fill(0),
            completed: Array(3).fill(false)
        };
        saveDailyGoals(dailyGoals);
    }

    return dailyGoals[today][userId];
}

function updateGoalProgress(userId, goalType, progress) {
    const dailyGoals = loadDailyGoals();
    const today = new Date().toDateString();

    if (!dailyGoals[today]) {
        dailyGoals[today] = {};
    }

    if (!dailyGoals[today][userId]) {
        dailyGoals[today][userId] = getUserDailyGoals(userId);
    }

    const userGoals = dailyGoals[today][userId];
    const goalIndex = userGoals.goals.findIndex(goal => goal.type === goalType);

    if (goalIndex !== -1) {
        userGoals.progress[goalIndex] = Math.min(userGoals.progress[goalIndex] + progress, userGoals.goals[goalIndex].count);

        if (userGoals.progress[goalIndex] >= userGoals.goals[goalIndex].count && !userGoals.completed[goalIndex]) {
            userGoals.completed[goalIndex] = true;
            giveReward(userId, userGoals.goals[goalIndex].reward);
        }

        dailyGoals[today][userId] = userGoals;
        saveDailyGoals(dailyGoals);
    }
}


client.on('messageCreate', async (message) => {
    if (!message.author.bot) {
        updateGoalProgress(message.author.id, 'messages', 1);
    }
});


const guildInvites = new Map();

client.on(Events.InviteCreate, async invite => {
    const invites = await invite.guild.invites.fetch();
    const codeUses = new Map();
    invites.each(inv => codeUses.set(inv.code, inv.uses));
    guildInvites.set(invite.guild.id, codeUses);
});

client.once(Events.ClientReady, () => {
    client.guilds.cache.forEach(guild => {
        guild.invites.fetch()
            .then(invites => {
                const codeUses = new Map();
                invites.each(inv => codeUses.set(inv.code, inv.uses));
                guildInvites.set(guild.id, codeUses);
            })
            .catch(err => {
                return;
            });
    });
});

client.on(Events.GuildMemberAdd, async member => {
    const cachedInvites = guildInvites.get(member.guild.id) || new Map();
    const newInvites = await member.guild.invites.fetch();

    try {
        const usedInvite = newInvites.find(inv => cachedInvites.get(inv.code) < inv.uses);

        if (usedInvite && activeInviteEvent) {
            const inviterId = usedInvite.inviter.id;
            const invitedUserId = member.id;

            if (!activeInviteEvent.uniqueInvitedUsers.has(invitedUserId)) {
                if (!activeInviteEvent.userInvites[inviterId]) {
                    activeInviteEvent.userInvites[inviterId] = 0;
                }
                activeInviteEvent.userInvites[inviterId]++;
                activeInviteEvent.uniqueInvitedUsers.add(invitedUserId);

                updateGoalProgress(usedInvite.inviter.id, 'invites', 1);
                saveInviteEvent(activeInviteEvent);
            } else {
                return;
            }
        }
    } catch (err) {
        return;
    }

    newInvites.each(inv => cachedInvites.set(inv.code, inv.uses));
    guildInvites.set(member.guild.id, cachedInvites);
});

client.on('messageReactionAdd', async (reaction, user) => {
    try {
        if (user.bot) return;
        if (reaction.partial) {
            try {
                await reaction.fetch();
            } catch (error) {
                return;
            }
        }
        if (tradeCounts[user.id] && tradeCounts[user.id].code) {
            updateGoalProgress(user.id, 'reactions', 1);
        }
    } catch (error) {
        return;
    }
});

function scheduleNewDailyGoals() {
    const now = new Date();
    const night = new Date(
        now.getFullYear(),
        now.getMonth(),
        now.getDate() + 1,
        0, 0, 0
    );
    const msToMidnight = night.getTime() - now.getTime();

    setTimeout(() => {
        generateDailyGoals();
        scheduleNewDailyGoals();
    }, msToMidnight);
}


function giveReward(userId, amount) {
    if (!tradeCounts[userId]) {
        tradeCounts[userId] = { botcoins: 0 };
    }

    tradeCounts[userId].botcoins += amount;
}


scheduleNewDailyGoals();


const INVITE_EVENT_FILE = path.join(__dirname, 'inviteEvent.json');

function loadInviteEvent() {
    try {
        const data = fs.readFileSync(INVITE_EVENT_FILE, 'utf8');
        const event = JSON.parse(data);
        if (event && event.uniqueInvitedUsers) {
            event.uniqueInvitedUsers = new Set(event.uniqueInvitedUsers);
        }
        return event;
    } catch (error) {
        if (error.code === 'ENOENT') {
            return null;
        }
        return null;
    }
}

function saveInviteEvent(event) {
    if (event) {
        const eventToSave = {
            ...event,
            uniqueInvitedUsers: Array.from(event.uniqueInvitedUsers)
        };
        fs.writeFileSync(INVITE_EVENT_FILE, JSON.stringify(eventToSave, null, 2));
    } else {
        fs.writeFileSync(INVITE_EVENT_FILE, JSON.stringify(null));
    }
}



const wheelPrizes = ['0.5x', '0.5x', '0.5x', '0.1x', '0.1x', '0.1x', '0.1x', '1x', '1x', '1.5x', '2x', 'Jackpot', 'Lose', 'Lose', 'Lose', 'Lose', 'Lose'];

async function spinWheel(interaction) {
    const userId = interaction.user.id;
    const userData = tradeCounts[userId];

    loadBetLimits();

    if (!canUserBet(userId)) {
        const betLimitEmbed = {
            embeds: [{
                title: 'Bet limit reached',
                description: `You have reached the limit of **${maxBetsPerHour}** bets per hour. Please try again later`,
                color: 0xD32F2F
            }]
        };
        await interaction.reply(betLimitEmbed);
        return;
    }

    if (!userData || typeof userData !== 'object' || !userData.code) {
        const registerEmbed = {
            title: 'Registration required',
            color: 0xD32F2F,
            description: 'You must register first using **/smoq register**',
        };
        await interaction.reply({ embeds: [registerEmbed] });
        return;
    }

    const betAmount = interaction.options.getInteger('amount');

    if (userData.botcoins < betAmount) {
        const insufficientFundsEmbed = {
            title: 'Insufficient botcoins',
            color: 0xD32F2F,
            description: 'You do not have enough botcoins to place this bet',
        };
        await interaction.reply({ embeds: [insufficientFundsEmbed] });
        return;
    }

    recordBet(userId);

    const spinResult = wheelPrizes[Math.floor(Math.random() * wheelPrizes.length)];

    const wheelEmbed = {
        title: 'Wheel of fortune',
        color: 0xf2f290,
        description: 'Spinning the wheel...',
    };
    const message = await interaction.reply({ embeds: [wheelEmbed] });

    for (let i = 0; i < 10; i++) {
        await message.edit({ embeds: [{ ...wheelEmbed, description: `Spinning... **${wheelPrizes[i % wheelPrizes.length]}**` }] });
        await new Promise(resolve => setTimeout(resolve, 200));
    }

    let winAmount = 0;
    let resultDescription = '';

    switch (spinResult) {
        case 'Jackpot':
            winAmount = betAmount * 5;
            resultDescription = `Congratulations! You hit the jackpot and won **${winAmount}** botcoins!`;
            break;
        case 'Lose':
            winAmount = -betAmount;
            resultDescription = `Oh no! You lost your bet of **${betAmount}** botcoins`;
            break;
        default:
            const multiplier = parseFloat(spinResult);
            winAmount = Math.floor(betAmount * multiplier) - betAmount;
            if (winAmount > 0) {
                resultDescription = `You won **${winAmount}** botcoins!`;
            } else if (winAmount < 0) {
                resultDescription = `You lost **${-winAmount}** botcoins`;
            } else {
                resultDescription = `You broke even`;
            }
    }

    userData.botcoins += winAmount;
    saveTradeLog(tradeCounts);

    const resultEmbed = {
        title: 'Wheel of fortune result',
        color: winAmount >= 0 ? 0x00AE86 : 0xD32F2F,
        description: `The wheel landed on **${spinResult}**\n\n${resultDescription}\n\nYour new balance is **${userData.botcoins}** botcoins`,
    };
    await message.edit({ embeds: [resultEmbed] });

    saveBetLimits();
}


let activeInviteEvent = loadInviteEvent();
async function startInviteEvent(interaction) {
    const userId = interaction.user.id;

    if (!isAdmin(userId)) {
        const notAdminEmbed = {
            title: 'Access denied',
            color: 0xD32F2F,
            description: 'You do not have permission to run this command',
        };
        await interaction.reply({ embeds: [notAdminEmbed], ephemeral: true });
        return;
    }

    if (activeInviteEvent) {
        const eventActiveEmbed = {
            title: 'Event already active',
            color: 0xD32F2F,
            description: 'An invite event is already active',
        };
        await interaction.reply({ embeds: [eventActiveEmbed] });
        return;
    }

    const duration = interaction.options.getInteger('duration');
    const invitesRequired = interaction.options.getInteger('invitesreq');
    const tradesReward = interaction.options.getInteger('tradesrw');

    if (!duration || !invitesRequired || !tradesReward) {
        const missingParamsEmbed = {
            title: 'Missing parameters',
            color: 0xD32F2F,
            description: 'Please provide all required parameters: duration (in hours), invites required, and trades reward',
        };
        await interaction.reply({ embeds: [missingParamsEmbed] });
        return;
    }

    activeInviteEvent = {
        startTime: Date.now(),
        endTime: Date.now() + duration * 60 * 60 * 1000,
        invitesRequired,
        tradesReward,
        userInvites: {},
        uniqueInvitedUsers: new Set()
    };

    saveInviteEvent(activeInviteEvent);

    const eventEmbed = {
        title: 'Invite event started',
        color: 0x00AE86,
        description: `Invite your friends to earn trades!\n\n` +
            `Every **${invitesRequired}** invites = **${tradesReward}** trades\n` +
            `Event ends <t:${Math.floor(activeInviteEvent.endTime / 1000)}:R>\n\n` +
            `Use **/smoq claim-invites** to claim your rewards!`,
    };

    await interaction.reply({ embeds: [eventEmbed] });

    setTimeout(() => endInviteEvent(interaction.channel), activeInviteEvent.endTime - Date.now());
}

async function endInviteEvent(channel) {
    activeInviteEvent = null;
    saveInviteEvent(null);
    await channel.send('The invite event has ended!');
}


function checkExpiredEvent() {
    if (activeInviteEvent && Date.now() > activeInviteEvent.endTime) {
        activeInviteEvent = null;
        saveInviteEvent(null);
    }
}
async function claimInvites(interaction) {
    const userId = interaction.user.id;
    const userData = tradeCounts[userId];

    if (!userData || typeof userData !== 'object' || !userData.code) {
        const registerEmbed = {
            title: 'Registration required',
            color: 0xD32F2F,
            description: 'You must register first using **/smoq register**',
        };
        await interaction.reply({ embeds: [registerEmbed] });
        return;
    }

    if (!activeInviteEvent) {
        const noEventEmbed = {
            title: 'No active event',
            color: 0xD32F2F,
            description: 'There is no active invite event at the moment',
        };
        await interaction.reply({ embeds: [noEventEmbed] });
        return;
    }

    const userInvites = activeInviteEvent.userInvites[userId] || 0;
    const rewardMultiplier = Math.floor(userInvites / activeInviteEvent.invitesRequired);
    const totalReward = rewardMultiplier * activeInviteEvent.tradesReward;

    if (rewardMultiplier === 0) {
        const notEnoughInvitesEmbed = {
            title: 'Not enough invites',
            color: 0xD32F2F,
            description: `You haven't invited enough people yet. You need **${activeInviteEvent.invitesRequired}** invites to get a reward\n` +
                `You currently have **${userInvites}** invites`,
        };
        await interaction.reply({ embeds: [notEnoughInvitesEmbed] });
        return;
    }


    userData.trades_remaining += totalReward;


    activeInviteEvent.userInvites[userId] = userInvites % activeInviteEvent.invitesRequired;

    const claimEmbed = {
        title: 'Invite rewards claimed',
        color: 0x00AE86,
        description: `You've successfully claimed **${totalReward}** trades!\n\n` +
            `Invites used: **${rewardMultiplier * activeInviteEvent.invitesRequired}**\n` +
            `Remaining invites: **${activeInviteEvent.userInvites[userId]}**\n\n` +
            `You currently have **${activeInviteEvent.userInvites[userId]}** invites`,
    };

    await interaction.reply({ embeds: [claimEmbed] });
    saveTradeLog(tradeCounts);
}

const DAILY_LOGIN_FILE = path.join(__dirname, 'dailyLoginData.json');

function loadDailyLoginData() {
    try {
        const data = fs.readFileSync(DAILY_LOGIN_FILE, 'utf8');
        return JSON.parse(data);
    } catch (error) {
        return {};
    }
}

function saveDailyLoginData(data) {
    fs.writeFileSync(DAILY_LOGIN_FILE, JSON.stringify(data, null, 2));
}

async function dailyLogin(interaction) {
    const userId = interaction.user.id;
    const userTradeData = tradeCounts[userId];

    if (!userTradeData || typeof userTradeData !== 'object' || !userTradeData.code) {
        const registerEmbed = {
            title: 'Registration required',
            color: 0xD32F2F,
            description: 'You must register first using **/smoq register**',
        };
        await interaction.reply({ embeds: [registerEmbed] });
        return;
    }

    const now = new Date();
    const dailyLoginData = loadDailyLoginData();

    if (!dailyLoginData[userId]) {
        dailyLoginData[userId] = { lastLogin: null, consecutiveDays: 0 };
    }

    const userLoginData = dailyLoginData[userId];
    const lastLogin = userLoginData.lastLogin ? new Date(userLoginData.lastLogin) : null;

    if (!lastLogin || now.toDateString() !== lastLogin.toDateString()) {
        userLoginData.consecutiveDays++;
        if (userLoginData.consecutiveDays > 7) {
            userLoginData.consecutiveDays = 1;
        }

        const reward = calculateReward(userLoginData.consecutiveDays);
        giveReward(userId, reward);

        userLoginData.lastLogin = now.toISOString();
        saveDailyLoginData(dailyLoginData);

        const embed = {
            title: 'Daily login reward',
            color: 0x00AE86,
            description: `You've received **${reward}** botcoins for your day **${userLoginData.consecutiveDays}** login!`,
            footer: { text: 'Come back tomorrow for your next reward!' }
        };

        await interaction.reply({ embeds: [embed] });
    } else {
        const embed = {
            title: 'Daily login',
            color: 0xD32F2F,
            description: 'You have already claimed your daily reward today. Come back tomorrow!',
        };

        await interaction.reply({ embeds: [embed] });
    }
}

function calculateReward(day) {
    const rewards = [10, 15, 20, 25, 30, 35, 50];
    return rewards[day - 1];
}

async function checkWallet(interaction) {
    if (!hasBotPerms(interaction.member)) {
        const noPermsEmbed = {
            title: 'Access denied',
            color: 0xD32F2F,
            description: 'You need bot perms to use this command',
        };
        await interaction.reply({ embeds: [noPermsEmbed] });
        return;
    }

    const targetUser = interaction.options.getUser('user');
    const userData = tradeCounts[targetUser.id];

    if (!userData) {
        const notRegisteredEmbed = {
            title: 'User not registered',
            color: 0xD32F2F,
            description: `${targetUser.username} is not registered`,
        };
        await interaction.reply({ embeds: [notRegisteredEmbed] });
        return;
    }

    const walletEmbed = {
        title: `Wallet check - ${targetUser.username}`,
        color: 0x00AE86,
        fields: [
            {
                name: 'Botcoins',
                value: `**${userData.botcoins || 0}**`,
                inline: false
            },
            {
                name: 'Trades',
                value: `**${userData.trades_remaining || 0}**`,
                inline: false
            }
        ]
    };

    if (userData.code) {
        walletEmbed.fields.push({
            name: 'Registration status',
            value: '**Registered**',
            inline: false
        });
    }

    if (userData.expiration_date) {
        const expirationDate = new Date(userData.expiration_date);
        walletEmbed.fields.push({
            name: 'Expiration date',
            value: `<t:${Math.floor(expirationDate.getTime() / 1000)}:R>`,
            inline: false
        });
    }

    await interaction.reply({ embeds: [walletEmbed] });
}

async function freeTradeCommand(interaction) {
    if (!hasBotPerms(interaction.member)) {
        const noPermsEmbed = {
            title: 'Access denied',
            color: 0xD32F2F,
            description: 'You need bot perms to use this command',
        };
        await interaction.reply({ embeds: [noPermsEmbed] });
        return;
    }

    const userId = interaction.user.id;
    const userData = tradeCounts[userId];

    if (!userData?.code) {
        const registerEmbed = {
            title: 'Registration required',
            color: 0xD32F2F,
            description: 'You must register first using **/smoq register**'
        };
        await interaction.reply({ embeds: [registerEmbed] });
        return;
    }

    if (activeProcesses.has(userId)) {
        const busyEmbed = {
            title: 'Process in progress',
            color: 0xD32F2F,
            description: 'You have an active trading process - Please wait for it to complete'
        };
        await interaction.reply({ embeds: [busyEmbed] });
        return;
    }

    const amount = interaction.options.getInteger('amount');
    activeProcesses.add(userId);

    const processingEmbed = {
        title: 'Trades processing',
        color: 0x00AE86,
        description: `Processing **${amount}** trades with your personal bot code!`,
    };

    const reply = await interaction.reply({ embeds: [processingEmbed] });

    try {
        let currentToken = getCurrentToken();
        if (!currentToken) {
            await interaction.editReply({
                embeds: [{
                    title: 'Trade processing failed',
                    color: 0xD32F2F,
                    description: 'An error occurred during trade processing - Try again!'
                }]
            });
            return;
        }

        const pythonProcess = spawn('python3', ['rgbt-25.py', 'trades', amount.toString(), userData.code, currentToken]);

        const processResult = await new Promise((resolve, reject) => {
            let output = '';
            let errorOutput = '';

            pythonProcess.stdout.on('data', (data) => {
                output += data.toString();
                console.log(`stdout: ${data}`);
            });

            pythonProcess.stderr.on('data', (data) => {
                errorOutput += data.toString();
                console.error(`stderr: ${data}`);
            });

            pythonProcess.on('close', (exitCode) => {
                resolve({ exitCode, output, errorOutput });
            });

            pythonProcess.on('error', (error) => {
                reject(error);
            });
        });

        let tradesNotCompleted = 0;
        let tradesCompleted = amount;

        const tradesNotCompletedMatch = processResult.errorOutput.match(/tradesCompleted (\d+) tradesNotCompleted (\d+)/);
        if (tradesNotCompletedMatch) {
            tradesNotCompleted = parseInt(tradesNotCompletedMatch[2]);
            tradesCompleted = parseInt(tradesNotCompletedMatch[1]);
        }

        if (processResult.exitCode === 0) {
            if (tradesCompleted === amount) {
                await interaction.editReply({
                    embeds: [{
                        title: 'Trades completed',
                        color: 0x00AE86,
                        description: `Successfully processed **${tradesCompleted}** trades!`
                    }]
                });
            } else if (tradesCompleted > 0) {
                await interaction.editReply({
                    embeds: [{
                        title: 'Trades completed',
                        color: 0x00AE86,
                        description: `Successfully processed **${tradesCompleted}** trades!\n**${tradesNotCompleted}** trades could not be completed`
                    }]
                });
            } else {
                await interaction.editReply({
                    embeds: [{
                        title: 'Trades failed',
                        color: 0xD32F2F,
                        description: 'No trades could be processed'
                    }]
                });
            }
        } else {
            const newToken = changeToken();
            await interaction.editReply({
                embeds: [{
                    title: 'Trade processing failed',
                    color: 0xD32F2F,
                    description: 'An error occurred during trade processing - Try again!'
                }]
            });
        }
    } catch (error) {
        await interaction.editReply({
            embeds: [{
                title: 'Unexpected error',
                color: 0xD32F2F,
                description: 'An unexpected error occurred - Please contact support'
            }]
        });
    } finally {
        activeProcesses.delete(userId);
    }
}

const smoqCommand = new SlashCommandBuilder()
    .setName('smoq')
    .setDescription('Smoq Games')
    .addSubcommand(subcommand =>
        subcommand
            .setName('dspin')
            .setDescription('Perform a daily spin'))
    .addSubcommand(subcommand =>
        subcommand
            .setName('register')
            .setDescription('Register with the bot'))
    .addSubcommand(subcommand =>
        subcommand
            .setName('unregister')
            .setDescription('Unregister with the bot'))
    .addSubcommand(subcommand =>
        subcommand
            .setName('wallet')
            .setDescription('View your main wallet'))
    .addSubcommand(subcommand =>
        subcommand
            .setName('claim-bt')
            .setDescription('Perform a trade with the bot')
            .addIntegerOption(option =>
                option
                    .setName('amount')
                    .setDescription('Number of times you want the bot perform a trade with you (1-10)')
                    .setMinValue(1)
                    .setMaxValue(10)
                    .setRequired(true)
            ))
    .addSubcommand(subcommand =>
        subcommand
            .setName('claim-boosts')
            .setDescription('Claim free trades if you are a booster!'))
    .addSubcommand(subcommand =>
        subcommand
            .setName('daily-goals')
            .setDescription('View your daily goals'))
    .addSubcommand(subcommand =>
        subcommand
            .setName('claim-invites')
            .setDescription('Claim your invite rewards'))
    .addSubcommand(subcommand =>
        subcommand
            .setName('exchange')
            .setDescription('20 BC = 1 TRADE')
            .addIntegerOption(option =>
                option.setName('amount')
                    .setDescription('The amount of botcoins you want to exchange for trades')
                    .setRequired(true)))
    .addSubcommand(subcommand =>
        subcommand
            .setName('redeem-promocode')
            .setDescription('Redeem an active promocode')
            .addStringOption(option =>
                option.setName('promocode')
                    .setDescription('Put the promocode here')
                    .setRequired(true)))
    .addSubcommand(subcommand =>
        subcommand
            .setName('searchdb')
            .setDescription('Search for players in the database by the name')
            .addStringOption(option =>
                option.setName('name')
                    .setDescription('The name of the player to search in the db for')
                    .setRequired(true)))
    .addSubcommand(subcommand =>
        subcommand
            .setName('daily-login')
            .setDescription('Claim your daily login reward'));

const smoqGamesCommand = new SlashCommandBuilder()
    .setName('smoq-mg')
    .setDescription('Smoq MG')
    .addSubcommand(subcommand =>
        subcommand
            .setName('fishing')
            .setDescription('Play the fishing minigame!'))
    .addSubcommand(subcommand =>
        subcommand
            .setName('coinflip')
            .setDescription('Bet on heads or tails (BETTING!)')
            .addIntegerOption(option =>
                option.setName('amount')
                    .setDescription('The amount of botcoins you want to bet')
                    .setRequired(true)
                    .setMinValue(1)
                    .setMaxValue(20))
            .addStringOption(option =>
                option.setName('choice')
                    .setDescription('Your choice: heads or tails')
                    .setRequired(true)
                    .addChoices(
                        { name: 'heads', value: 'heads' },
                        { name: 'tails', value: 'tails' }
                    )))
    .addSubcommand(subcommand =>
        subcommand
            .setName('dice')
            .setDescription('Roll a dice and bet botcoins (BETTING!)')
            .addIntegerOption(option =>
                option.setName('amount')
                    .setDescription('The amount of botcoins you want to bet')
                    .setRequired(true)
                    .setMinValue(1)
                    .setMaxValue(20))
            .addIntegerOption(option =>
                option.setName('number')
                    .setDescription('Number you are betting on (1 to 6)')
                    .setRequired(true)
                    .setMinValue(1)
                    .setMaxValue(6)))
    .addSubcommand(subcommand =>
        subcommand
            .setName('roulette')
            .setDescription('Bet on a color in roulette (BETTING!)')
            .addIntegerOption(option =>
                option.setName('amount')
                    .setDescription('The amount of botcoins you want to bet')
                    .setRequired(true)
                    .setMinValue(1)
                    .setMaxValue(20))
            .addStringOption(option =>
                option.setName('color')
                    .setDescription('Color to bet on')
                    .setRequired(true)
                    .addChoices(
                        { name: 'Red', value: 'red' },
                        { name: 'Green', value: 'green' },
                        { name: 'Blue', value: 'blue' }
                    )))
    .addSubcommand(subcommand =>
        subcommand
            .setName('slots')
            .setDescription('Play the slots minigame (BETTING!)')
            .addIntegerOption(option =>
                option.setName('amount')
                    .setDescription('The amount of botcoins you want to bet')
                    .setRequired(true)
                    .setMinValue(1)
                    .setMaxValue(20)))
    .addSubcommand(subcommand =>
        subcommand
            .setName('crash')
            .setDescription('Play the crash minigame for botcoins (BETTING!)')
            .addIntegerOption(option =>
                option
                    .setName('amount')
                    .setDescription('The amount of botcoins you want to bet')
                    .setRequired(true)
                    .setMinValue(1)
                    .setMaxValue(20)))
    .addSubcommand(subcommand =>
        subcommand
            .setName('rps')
            .setDescription('Play rock paper scissors against the bot (BETTING!)')
            .addIntegerOption(option =>
                option.setName('amount')
                    .setDescription('Amount of botcoins to bet')
                    .setRequired(true)
                    .setMinValue(1)
                    .setMaxValue(20)))
    .addSubcommand(subcommand =>
        subcommand
            .setName('stw')
            .setDescription('Spin the wheel of fortune! (BETTING!)')
            .addIntegerOption(option =>
                option.setName('amount')
                    .setDescription('The amount of botcoins you want to bet')
                    .setRequired(true)
                    .setMinValue(1)
                    .setMaxValue(20)))

const smoqBotPermsCommand = new SlashCommandBuilder()
    .setName('bot-perms')
    .setDescription('Bot perms')
    .addSubcommand(subcommand =>
        subcommand
            .setName('openinv')
            .setDescription('Make an open invite with the bot (BOT PERMS ONLY!)')
            .addIntegerOption(option =>
                option.setName('minutes')
                    .setDescription('The number of minutes the OI will be active')
                    .setRequired(true)
                    .setMinValue(1)
                    .setMaxValue(10)
            ))
    .addSubcommand(subcommand =>
        subcommand
            .setName('pay')
            .setDescription('Grant trades and/or botcoins to users (BOT PERMS ONLY!)')
            .addUserOption(option =>
                option.setName('user')
                    .setDescription('The user to receive trades/botcoins')
                    .setRequired(true))
            .addStringOption(option =>
                option.setName('type')
                    .setDescription('What to give: trades, botcoins, or both')
                    .setRequired(true)
                    .addChoices(
                        { name: 'Trades', value: 'trades' },
                        { name: 'Botcoins', value: 'botcoins' },
                        { name: 'Both', value: 'both' }
                    ))
            .addIntegerOption(option =>
                option.setName('amount')
                    .setDescription('Amount to give')
                    .setRequired(true)))
    .addSubcommand(subcommand =>
        subcommand
            .setName('remove')
            .setDescription('Remove a specific amount of trades or botcoins from a user (BOT PERMS ONLY!)')
            .addUserOption(option =>
                option.setName('user')
                    .setDescription('The user from whom trades or botcoins will be removed')
                    .setRequired(true))
            .addStringOption(option =>
                option.setName('amount')
                    .setDescription('The number of trades or botcoins you want to remove from a user - Enter "all" to remove all')
                    .setRequired(true))
            .addStringOption(option =>
                option.setName('type')
                    .setDescription('Specify whether to remove trades, botcoins, or both')
                    .setRequired(true)
                    .addChoices(
                        { name: 'Trades', value: 'trades' },
                        { name: 'Botcoins', value: 'botcoins' },
                        { name: 'Both', value: 'both' }
                    )))
    .addSubcommand(subcommand =>
        subcommand
            .setName('check-wallet')
            .setDescription('Check wallet of a specific user (BOT PERMS ONLY!)')
            .addUserOption(option =>
                option
                    .setName('user')
                    .setDescription('The user whose wallet you want to check')
                    .setRequired(true)
            ))
    .addSubcommand(subcommand =>
        subcommand
            .setName('freetrade')
            .setDescription('Claim free trades! (BOT PERMS ONLY!)')
            .addIntegerOption(option =>
                option
                    .setName('amount')
                    .setDescription('Number of times you want the bot perform a trade with you (1-10)')
                    .setRequired(true)
                    .setMinValue(1)
                    .setMaxValue(10)
            )
    )

const smoqAdminCommand = new SlashCommandBuilder()
    .setName('admin')
    .setDescription('Smoq admin only')
    .addSubcommand(subcommand =>
        subcommand
            .setName('admin-pay')
            .setDescription('Grant trades and/or botcoins to users (ADMIN ONLY!)')
            .addUserOption(option =>
                option.setName('user')
                    .setDescription('The user to receive trades/botcoins')
                    .setRequired(true))
            .addStringOption(option =>
                option.setName('type')
                    .setDescription('What to give: trades, botcoins, or both')
                    .setRequired(true)
                    .addChoices(
                        { name: 'Trades', value: 'trades' },
                        { name: 'Botcoins', value: 'botcoins' },
                        { name: 'Both', value: 'both' }
                    ))
            .addIntegerOption(option =>
                option.setName('amount')
                    .setDescription('Amount to give')
                    .setRequired(true))
            .addStringOption(option =>
                option.setName('time')
                    .setDescription('Expiration date')
                    .setRequired(false)
                    .addChoices(
                        { name: '1 Day', value: '1 day' },
                        { name: '1 Week', value: '1 week' },
                        { name: '2 Weeks', value: '2 weeks' },
                        { name: '1 Month', value: '1 month' },
                        { name: '3 Months', value: '3 months' },
                        { name: '6 Months', value: '6 months' },
                        { name: '1 Year', value: '1 year' }
                    )))
    .addSubcommand(subcommand =>
        subcommand
            .setName('admin-remove')
            .setDescription('Remove a specific amount of trades or botcoins from a user (ADMIN ONLY!)')
            .addUserOption(option =>
                option.setName('user')
                    .setDescription('The user from whom trades or botcoins will be removed')
                    .setRequired(true))
            .addStringOption(option =>
                option.setName('amount')
                    .setDescription('The number of trades or botcoins you want to remove from a user - Enter "all" to remove all')
                    .setRequired(true))
            .addStringOption(option =>
                option.setName('type')
                    .setDescription('Specify whether to remove trades, botcoins, or both')
                    .setRequired(true)
                    .addChoices(
                        { name: 'Trades', value: 'trades' },
                        { name: 'Botcoins', value: 'botcoins' },
                        { name: 'Both', value: 'both' }
                    )))
    .addSubcommand(subcommand =>
        subcommand
            .setName('add-promocode')
            .setDescription('Create a new promocode (ADMIN ONLY!)')
            .addIntegerOption(option =>
                option.setName('bcoins')
                    .setDescription('Number of botcoins that the promocode will grant')
                    .setRequired(true))
            .addIntegerOption(option =>
                option.setName('duration')
                    .setDescription('Promocode duration in hours')
                    .setRequired(true))
            .addStringOption(option =>
                option.setName('code')
                    .setDescription('Custom code for the promocode')
                    .setRequired(true)))
    .addSubcommand(subcommand =>
        subcommand
            .setName('invite-event')
            .setDescription('Start an invite event (ADMIN ONLY!)')
            .addIntegerOption(option =>
                option.setName('duration')
                    .setDescription('Duration of the event in hours')
                    .setRequired(true))
            .addIntegerOption(option =>
                option.setName('invitesreq')
                    .setDescription('Number of invites required for a reward')
                    .setRequired(true))
            .addIntegerOption(option =>
                option.setName('tradesrw')
                    .setDescription('Number of trades to reward')
                    .setRequired(true)))

const commands = [smoqCommand, smoqGamesCommand, smoqAdminCommand, smoqBotPermsCommand];