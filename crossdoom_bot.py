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
    cwd = os.getcwd()
    with open('{}/crossdoom_config.json'.format(cwd), 'r') as f:
        temp = f.read()
        config_dict = json.loads(temp) # load guild configuration parameters
        temp = config_dict.get(str(message.guild.id), {'prefix':'c.'})  # return guild prefix, or default
        pref = temp['prefix']
    return pref

config_dict = configClass()  # To store configuration

# new: get prefix from config file. Default = '?'
bot = commands.Bot(command_prefix=(get_prefix), help_command=None)


@bot.event
async def on_ready():
    print('We have logged on as {0.user}'.format(bot))
    # # initial config (defaults)
    # Load config file if exist, otherwise create it
    cwd = os.getcwd()
    # print(cwd)  # DEBUG
    if os.path.isfile('{}/crossdoom_config.json'.format(cwd)):
        with open('{}/crossdoom_config.json'.format(cwd), 'r') as f:
            temp = f.read()
            config_dict.conf = json.loads(temp) # load guild configuration parameters
            print(config_dict.conf)  # DEBUG
    else:
        for guild in bot.guilds:  # create defaults for each guild if no config exists
            config_dict.conf[guild.id] = {}  # initialize guild
            config_dict.conf[guild.id]['prefix'] = 'c.'  # default prefix
            config_dict.conf[guild.id]['lang'] = 'ITA'  # default to ITA
            print('{}:{}\n{}'.format(guild, guild.id, config_dict.conf))  # DEBUG
        with open('{}/crossdoom_config.json'.format(cwd), 'w') as f:
            temp = json.dumps(config_dict.conf, indent=4, sort_keys=True)
            f.write(temp)


@bot.event
async def on_guild_join(guild): # when the bot joins the guild
    # Add guild to config class
    cwd = os.getcwd()
    config_dict.conf[guild.id] = {}  # initialize guild
    config_dict.conf[guild.id]['prefix'] = 'c.'  # default prefix
    config_dict.conf[guild.id]['lang'] = 'ITA'  # default to ITA
    with open('{}/crossdoom_config.json'.format(cwd), 'w') as f:  # write the config on file
        temp = json.dumps(config_dict.conf, f, indent=4, sort_keys=True)
        f.write(temp)


@bot.event
async def on_guild_remove(guild): # when the bot is removed from the guild
    # Remove guild to config class
    cwd = os.getcwd()
    _ = config_dict.conf.pop(str(guild.id))  # delete guild entry
    with open('{}/crossdoom_config.json'.format(cwd), 'w') as f:  # write the config on file
        temp = json.dumps(config_dict.conf, f, indent=4, sort_keys=True)
        f.write(temp)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('?'):  # Roll dice or destiny dice
        dice = message.content.split('?')[-1].strip()
        try:
            res = d20.roll(dice)
            await message.channel.send('Risultato: {}'.format(str(res)))
        except d20.errors.RollSyntaxError:
            if 'ds' in dice.lower():  # dado semaforo
                green, yellow, red = 0, 0, 0  # to store results
                num = dice.lower().split('ds')[0]
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
                        await message.channel.send('Risultato: {}'.format(result_string))
                    else:
                        await message.channel.send('Risultato: {}\n{}'.format(result_dice, result_string))
                except ValueError:
                    await message.channel.send('Inserire un\'espressione valida (prova `{}help`)'.format(
                                    config_dict.conf[str(message.guild.id)]['prefix']))
                    return
            else:
                await message.channel.send('Inserire un\'espressione valida (prova `{}help`)'.format(
                                config_dict.conf[str(message.guild.id)]['prefix']))
                return
    elif message.content.startswith('!'):  # Roll attack with Crossdoom rules
        # TODO: debug this function
        dice = message.content.split('!')[-1].strip()
        try:
            res = d20.roll(dice)
            dices = diceIterClass(res.expr.roll)  # Iterate and get dice values
            mess = ['Attacco:']
            for key in dices.initial_rolls.keys():
                if isinstance(key, int) and len(dices.initial_rolls[key]) > 0:
                    mess.append('{}d{}{} -> {}'.format(len(dices.initial_rolls[key]), key,
                                dices.initial_rolls[key], dices.crossdoom_rolls[key]))
            total = [sum(dices.crossdoom_rolls[x]) for x in dices.crossdoom_rolls if isinstance(x,int)]
            if sum(total) > 0:
                mess.append('Totale: {}'.format(sum(total)))
            else:
                mess.append('Attacco fallito.')
            dice_message = '\n'.join(mess)
            await message.channel.send(dice_message)
        except d20.errors.RollSyntaxError:
            await message.channel.send('Espressione non valida, consulta `{}help`'.format(
                            config_dict.conf[str(message.guild.id)]['prefix']))
    else:
        await bot.process_commands(message)  # Need this to process commands


# New help command (using embed)
@bot.command(name='help')
async def _help(ctx, arg=None):
    """Custom help command"""
    commands_names = [x.name for x in bot.commands]
    embed = discord.Embed(title='Help', color=discord.Colour.gold())
    # Italian Help
    print(config_dict.conf)  # DEBUG
    if config_dict.conf[str(ctx.guild.id)]['lang'] == 'ITA':
        if not arg:  # List all commands
            embed.add_field(name='Comandi per dadi:',
            value='- ?NdX per tirare N dadi a X facce.\n- ?Nds per tirare N dadi del destino.\n'+
            '- !NdX per tirare N dadi a X facce ed eseguire un attacco secondo le regole di Crossdoom')
            embed.add_field(name='Altri comandi (prefisso = \'{}\'):'.format(
                            config_dict.conf[str(ctx.guild.id)]['prefix']),
                            value='\n'.join(['{}. {}'.format(i, x) for i, x in enumerate(
                            commands_names, start=1)]), inline=False)
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
            embed.add_field(name='Commands list:',
                            value='\n'.join(['{}. {}'.format(i, x) for i, x in enumerate(
                            commands_names, start=1)]), inline=False)
            embed.add_field(name='Details', value='Write `{}help <command>` '.format(
                config_dict.conf[str(ctx.guild.id)]['prefix']) +
                'for more info about a specific command.')
        elif arg in commands_names:  # specific command help
            embed.add_field(name=arg, value=help_dict[arg][config_dict.conf[str(ctx.guild.id)]['lang']])
        else:
            embed.add_field(name='Well...', value='Command {} does not exist'.format(arg))
    await ctx.send(embed=embed)


@bot.command(name='quit', brief='-> Disconnetti il bot')
@commands.is_owner()  # just the bot owner has permission
async def _quit(ctx):
    """Disconnette il bot dal server."""
    await bot.logout()
# Error handling
@_quit.error
async def quit_error(ctx, error):
    if isinstance(error, commands.CheckFailure):  # if user has no permissions
        ctx.send('{}, non hai i permessi per questo comando'.format(ctx.author))
        # if you are not the owner, do not logout


# NEW (secure) method to load token using .env file
ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)
bot_token = os.getenv('GRIFONE_TOKEN')
bot.run(bot_token)
