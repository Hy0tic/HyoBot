import discord
import os
import json
from dotenv import load_dotenv
from discord.ext import commands

intents = discord.Intents.all()
env_vars = load_dotenv('.env')

with open('credentials.json', 'r') as file:
    credentials = json.load(file)
BOT = commands.Bot(command_prefix='!!', intents=intents)

@BOT.event
async def on_ready():
    await BOT.change_presence(status=discord.Status.online,
                              activity=discord.Game('with alligators | !!help'))
    print('{0.user} reporting for duty'.format(BOT))

@BOT.event
async def on_message(message):
    if message.author == BOT.user:
        return ()
    print(f'Message from {message.author}: {message.content}')
    await BOT.process_commands(message)

@BOT.event
async def setup_hook():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await BOT.load_extension(f'cogs.{filename[:-3]}')

@BOT.event
async def on_presence_update(before, after):
    game = str(after.activity)
    userId = after.id
    user = BOT.get_user(userId)
    if "overwatch" in game:
        print("overwatch detected")
        # await user.send("get off overwatch")

@BOT.command()
async def ping(ctx):
    await ctx.send('pong')


token = os.environ.get("Token")
BOT.run(token)
