from dotenv import load_dotenv, find_dotenv
import discord
import json
from discord.ext import commands
from discord.ext.commands import Bot
import random
import os
import d20
from games import diceIterClass, configClass
from help_dict import help_dict  # new help

# Helper function to get prefix from config file
def get_prefix(client, message):
    with open('guild_config.json', 'r') as f:
        temp = f.read()
        config_dict = json.loads(temp) # load guild configuration parameters
        temp = config_dict.get(str(message.guild.id), {'prefix':'g.'})  # return guild prefix, or default
        pref = temp['prefix']
    return pref


config_dict = configClass()

# new: get prefix from config file. Default = '?'
bot = commands.Bot(command_prefix=(get_prefix), help_command=None)


@bot.event
async def on_ready():
    print('We have logged on as {0.user}'.format(bot))
    # # initial config (defaults)
    # Load config file if exist, otherwise create it
    cwd = os.getcwd()
    if os.path.isfile('{}/guild_config.json'.format(cwd)):
        with open('{}/guild_config.json'.format(cwd), 'r') as f:
            temp = f.read()
            config_dict.conf = json.loads(temp) # load guild configuration parameters
            print(config_dict.conf)  # DEBUG
    else:
        for guild in bot.guilds:  # create defaults for each guild if no config exists
            config_dict.conf[guild.id] = {}  # initialize guild
            config_dict.conf[guild.id]['prefix'] = 'g.'  # default prefix
            config_dict.conf[guild.id]['lang'] = 'ITA'  # default to ITA
            print('{}:{}\n{}'.format(guild, guild.id, config_dict.conf))  # DEBUG
        with open('{}/guild_config.json'.format(cwd), 'w') as f:
            temp = json.dumps(config_dict.conf, indent=4, sort_keys=True)
            f.write(temp)


@bot.event
async def on_guild_join(guild): # when the bot joins the guild
    # Add guild to config class
    cwd = os.getcwd()
    config_dict.conf[guild.id] = {}  # initialize guild
    config_dict.conf[guild.id]['prefix'] = '?'  # default prefix
    config_dict.conf[guild.id]['lang'] = 'ITA'  # default to ITA
    with open('{}/guild_config.json'.format(cwd), 'w') as f:  # write the config on file
        temp = json.dumps(config_dict.conf, f, indent=4, sort_keys=True)
        f.write(temp)


@bot.event
async def on_guild_remove(guild): # when the bot is removed from the guild
    # Remove guild to config class
    cwd = os.getcwd()
    _ = config_dict.conf.pop(str(guild.id))  # delete guild entry
    with open('{}/guild_config.json'.format(cwd), 'w') as f:  # write the config on file
        temp = json.dumps(config_dict.conf, f, indent=4, sort_keys=True)
        f.write(temp)


# New help command (using embed)
@bot.command(name='help', aliases=['h'])
async def _help(ctx, arg=None):
    """Custom help command"""
    commands_names = [x.name for x in bot.commands]
    commands_aliases = [x.aliases for x in bot.commands]
    print('{}\n{}'.format(commands_names, commands_aliases))  # DEBUG
    embed = discord.Embed(title='Help', color=discord.Colour.gold())
    # Italian Help
    print(config_dict.conf)  # DEBUG
    if config_dict.conf[str(ctx.guild.id)]['lang'] == 'ITA':
        if not arg:  # List all commands
            embed.add_field(name='Prefisso: {}'.format(config_dict.conf[str(ctx.guild.id)]['prefix']),
            value='** **')

            # Add aliases to command name (if exist)
            comms = ['{}. {}'.format(i, x) for i, x in enumerate(commands_names, start=1)]
            for _i, com in enumerate(comms):
                if len(commands_aliases[_i]) > 0:
                    comms[_i] = '{}({})'.format(comms[_i], ','.join(commands_aliases[_i]))

            embed.add_field(name='Lista dei comandi:', value='\n'.join(comms), inline=False)
            embed.add_field(name='Dettagli', value='Scrivi `{}help <comando>` '.format(
                config_dict.conf[str(ctx.guild.id)]['prefix']) +
                'per maggiori informazioni su uno specifico comando.')
        elif arg in commands_names:  # specific command help
            embed.add_field(name=arg, value=help_dict[arg][config_dict.conf[str(ctx.guild.id)]['lang']])
        else:
            embed.add_field(name='Well...', value='Il comando {} non esiste'.format(arg))
    # English Help
    elif config_dict.conf[str(ctx.guild.id)]['lang'] == 'ENG':
        if not arg:  # List all commands
            embed.add_field(name='Prefix: {}'.format(config_dict.conf[str(ctx.guild.id)]['prefix']),
            value='** **')

            # Add aliases to command name (if exist)
            comms = ['{}. {}'.format(i, x) for i, x in enumerate(commands_names, start=1)]
            for _i, com in enumerate(comms):
                if len(commands_aliases[_i]) > 0:
                    comms[_i] = '{} ({})'.format(comms[_i], ', '.join(commands_aliases[_i]))

            embed.add_field(name='Commands list:', value='\n'.join(comms), inline=False)
            embed.add_field(name='Details', value='Write `{}help <command>` '.format(
                config_dict.conf[str(ctx.guild.id)]['prefix']) +
                'for more info about a specific command.')
        elif arg in commands_names:  # specific command help
            embed.add_field(name=arg, value=help_dict[arg][config_dict.conf[str(ctx.guild.id)]['lang']])
        else:
            embed.add_field(name='Well...', value='Command {} does not exist'.format(arg))
    await ctx.send(embed=embed)


# New implementation using d20
@bot.command(name='roll', brief='-> Tira un dado', aliases=['r'])
async def _roll(ctx, dice: str):
    """Tira un dado usando un'espressione del tipo NdX:
- N: numero di dadi [int]
- X: tipo di dado [int o 's']
     l'espressione Nds viene usata per tirare N dadi semaforo.

Restituisce: singoli valori e somma dei tiri

Per maggiori informazioni sulla sintassi utilizzata:
https://d20.readthedocs.io/en/latest/start.html#dice-syntax
"""
    try:
        res = d20.roll(dice)
        await ctx.send('Risultato: {}'.format(str(res)))
    except d20.errors.RollSyntaxError:
        if 'ds' in dice.lower():  # dado semaforo
            green, yellow, red = 0, 0, 0  # to store results
            num = dice.split('ds')[0]
            try:
                num = int(num)
                for i in range(num):
                    roll = random.randint(1, 6)
                    if roll <=3:
                        green += 1
                    elif 3 < roll <= 5:
                        yellow += 1
                    else:
                        red += 1
                result_dice = '  '.join(['🟩']*green + ['🟧']*yellow + ['🟥']*red)
                result_string = ', '.join(['**Verde** = {}'.format(green)]*(green>0) +
                                          ['**Giallo** = {}'.format(yellow)]*(yellow>0) +
                                          ['**Rosso** = {}'.format(red)]*(red>0))
                if num > 10:
                    await ctx.send('Risultato: {}'.format(result_string))
                else:
                    await ctx.send('Risultato: {}\n{}'.format(result_dice, result_string))

            except ValueError:
                await ctx.send('Inserire un\'espressione valida (prova `{}help`)'.format(
                            config_dict.conf[str(message.guild.id)]['prefix']))
                return
        else:
            await ctx.send('Inserire un\'espressione valida (prova `{}help`)'.format(
                            config_dict.conf[str(message.guild.id)]['prefix']))
            return


@bot.command(name='attack', brief='-> Tira dadi e usa le regole di Crossdoom per l\'attacco',
             aliases=['atk'])
async def _attack(ctx, dice: str):
    #TODO: debug this command. Sometimes it raises an error
    """Tira un dado usando un'espressione (vedi `help r`) e calcola
il risultato dell'attacco secondo il regolamento di Crossdoom.

Restituisce: singoli valori e risultato dell'attacco

Per maggiori informazioni sulla sintassi utilizzata:
https://d20.readthedocs.io/en/latest/start.html#dice-syntax
Per il regolamento di Crossdoom:
https://www.crossdoom.it/
"""
    try:
        res = d20.roll(dice)
        dices = diceIterClass(res.expr.roll)  # Iterate and get dice values
        message = ['Attacco:']
        for key in dices.initial_rolls.keys():
            if isinstance(key, int) and len(dices.initial_rolls[key]) > 0:
                message.append('{}d{}{} -> {}'.format(len(dices.initial_rolls[key]), key,
                               dices.initial_rolls[key], dices.crossdoom_rolls[key]))
        total = [sum(dices.crossdoom_rolls[x]) for x in dices.crossdoom_rolls if isinstance(x,int)]
        if sum(total) > 0:
            message.append('Totale: {}'.format(sum(total)))
        else:
            message.append('Attacco fallito.')
        dice_message = '\n'.join(message)
        await ctx.send(dice_message)
    except d20.errors.RollSyntaxError:
        await ctx.send('Espressione non valida, consulta `g.help roll`')


@bot.command(name='ghost', aliases=['gh'])
async def _ghost(ctx, N: int):
    """Tira N dadi a sei facce per il gioco di ruolo Ghostbusters."""
    gb_logo = bot.get_emoji(802986879808569385)  # check custom emoji ID
    roll_map = {1: '1️⃣', 2: '2️⃣', 3: '3️⃣', 4: '4️⃣', 5: '5️⃣', 6: '6️⃣', 'ghost': '{}'.format(gb_logo)}
    rolls = [random.randint(1,6) for _i in range(N-1)]  # normal rolls
    ghost_die = random.randint(1,6)
    roll_icons = ''
    roll_text = '('
    for dice in rolls:
        roll_icons += '{} '.format(roll_map[dice])
        roll_text += '{}, '.format(dice)
    roll_text += '**{}**)'.format(ghost_die)
    if ghost_die == 6:
        roll_icons += '{}'.format(roll_map['ghost'])
    else:
        roll_icons += '{}'.format(roll_map[ghost_die])
    if config_dict.conf[str(ctx.guild.id)]['lang'] == 'ITA':
        await ctx.send('{}\n**Risultato:** {}, tot = {}'. format(
                        roll_icons, roll_text, sum(rolls)+ghost_die))
    elif config_dict.conf[str(ctx.guild.id)]['lang'] == 'ENG':
        await ctx.send('{}\n**Result:** {}, tot = {}'. format(
                        roll_icons, roll_text, sum(rolls)+ghost_die))


@bot.command(name='quit', brief='-> Disconnetti il bot')
@commands.is_owner()  # just the bot owner has permission
async def _quit(ctx):
    """Disconnette il bot dal server e lascia una citazione. Punti extra se si indovina la fonte."""
    with open('quote.txt', 'r') as quotes:
        lines = quotes.readlines()
        await ctx.send('{}'.format(lines.pop(random.randint(0, len(lines)-1))))
    await bot.logout()
# Error handling
@_quit.error
async def quit_error(ctx, error):
    if isinstance(error, commands.CheckFailure):  # if user has no permissions
        with open('quote.txt', 'r') as quotes:
            lines = quotes.readlines()
            await ctx.send('{}'.format(lines.pop(random.randint(0, len(lines)-1))))
        # if you are not the owner, do not logout


@bot.command(name='deal', brief='-> Assegna carte')
async def _deal(ctx, N: int):
    """Pesca N carte da un mazzo preesistente nel canale e le assegna all'autore del comando.
WORK IN PROGRESS
"""
    await ctx.send('COMING SOON (Just a test to see if the command works)')


# NEW (secure) method to load token using .env file
ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)
bot_token = os.getenv('GRIFONE_TOKEN')
bot.run(bot_token)
