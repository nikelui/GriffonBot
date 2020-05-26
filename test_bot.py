import discord  

client = discord.Client()
with open('token.txt', 'r') as tk:
    token = tk.read()

@client.event
async def on_ready():
    print('We have logged on as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('!hello'):
        await message.channel.send('Hello, sucker!')

client.run(token)

