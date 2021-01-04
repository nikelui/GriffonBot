from discord.ext import commands
import random
import d20

bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print('We have logged on as {0.user}'.format(bot))


@bot.command(name='help')
async def _help(ctx, arg=""):
    if arg == "":
        embed = discord.Embed(
            title="Help",
            description="Help description",
            colour=discord.Colour.blurple()
        )
        embed.add_field(name="u.join", value="Join a game",inline=True)
        embed.add_field(name="u.start", value="Start a game", inline=True)
        await ctx.channel.send(embed=embed)


# New implementation using d20
@bot.command(name='roll')
async def _roll(ctx, dice: str):
    try:
        res = d20.roll(dice)
        await ctx.send('Result: {}'.format(str(res)))
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
                result_string = ', '.join(['**Green** = {}'.format(green)]*(green>0) + 
                                         ['**Yellow** = {}'.format(yellow)]*(yellow>0) +
                                         ['**Red** = {}'.format(red)]*(red>0))
                if num > 15:
                    await ctx.send('Result: {}'.format(result_string))
                else:
                    await ctx.send('Result: {}\n{}'.format(result_dice, result_string))
                
            except ValueError:
                await ctx.send('Enter a valid dice expression (try !help)')
                return
        else:
            await ctx.send('Enter a valid dice expression (try !help)')
            return


@bot.command(name='quit')
async def _quit(ctx):
    with open('goodbyes.txt', 'r') as quotes:
        lines = quotes.readlines()
        await ctx.send('{}'.format(lines.pop(random.randint(0, len(lines)-1))))
    await bot.logout()


@bot.command(name='deal')
async def _deal(ctx):
    await ctx.send('Just a test to see if the command works')

with open('token.txt', 'r') as tk:
    token = tk.read()
bot.run(token)
