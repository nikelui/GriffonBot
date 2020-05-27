from discord.ext import commands
import random, re

bot = commands.Bot(command_prefix='!')

with open('token.txt', 'r') as tk:
    token = tk.read()

@bot.event
async def on_ready():
    print('We have logged on as {0.user}'.format(bot))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.startswith('!hello'):
        await message.channel.send('Hello, sucker!')
    await bot.process_commands(message) # need this to work
    
@bot.command(name='roll')
async def _roll(ctx, *, dice: str):
    dice_rolls = [] # to store the dice rolls
    dice_val = [] # to store the dice strings
    dice_pos = [] # to store the dice strings position
    # Some regex magic
    pattern = '[0-9]+?d[0-9]+' # hopefully the range works
    dices = [x for x in re.finditer(pattern, dice)] # match objects
    for d in dices:
    
    	dice_val.append(d.string[d.start():d.end()]) # save dice string
    	dice_pos.append((d.start(), d.end())) # save position as tuples
    	
    	num, lim = dice_val[-1].split('d') # separate num and dice type
    	if num == '':
    		num = '1' # assume 1 if none is provided
    	num, lim = map(int, [num, lim]) # convert to int
    	
    	# Roll the dices
    	dice_rolls.append(tuple([random.randint(1,lim) for x in range(num)]))
	
	# compose message
    mess = []
    for i,dice in enumerate(dice_val):
        mess.append('{} ({})'.format(str(dice_rolls[i]), sum(dice_rolls[i])))
    mess.append('Sum: {}'.format(sum([sum(x) for x in dice_rolls])))
    await ctx.send('\n'.join(mess))

@bot.command(name='quit')
async def _quit(ctx):
    await bot.logout()

@bot.command()
async def deal(ctx):
    await ctx.send('Just a test to see if the command works')

bot.run(token)

