from discord.ext import commands
from dotenv import load_dotenv, find_dotenv
import discord
import random
import os
import d20
from games import diceIterClass


class MyHelpCommand(commands.DefaultHelpCommand):    
    def get_ending_note(self):
        return 'Scrivi `g.help <comando>` per avere più informazioni su uno specifico comando.'
    def command_not_found(self, command):
        return f'Comando <{command}> non trovato'


help_command = MyHelpCommand(brief='-> Mostra questo messaggio',
    no_category = 'Comandi', commands_heading = 'Comandi')

bot = commands.Bot(command_prefix='g.', help_command=help_command)


@bot.event
async def on_ready():
    print('We have logged on as {0.user}'.format(bot))
## Uncomment to change avatar
#    with open('img/icon.png', 'rb') as f:
#        image = f.read()
#        await bot.user.edit(avatar=image)


# New implementation using d20
@bot.command(name='roll', brief='-> Tira un dado')
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
        if 'ds' in dice:  # dado semaforo
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
                await ctx.send('Inserire un\'espressione valida (prova `g.help`)')
                return
        else:
            await ctx.send('Inserire un\'espressione valida (prova `g.help`)')
            return


@bot.command(name='attack', brief='-> Tira dadi e usa le regole di Crossdoom per l\'attacco')
async def _attack(ctx, dice: str):
    """Tira un dado usando un'espressione (vedi g.help roll) e calcola
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
async def stop_error(ctx, error):
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
    await ctx.send('Just a test to see if the command works')


# NEW (secure) method to load token using .env file
ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)
bot_token = os.getenv('BOT_TOKEN')
bot.run(bot_token)
