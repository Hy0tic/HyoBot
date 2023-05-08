import discord
import os
import requests
import json
from discord.ext import commands

intents = discord.Intents.all()

with open('credentials.json', 'r') as file:
    credentials = json.load(file)
BOT = commands.Bot(command_prefix='!!', intents=intents)

@BOT.event
async def on_ready():
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

@BOT.command()
async def ping(ctx):
    await ctx.send('pong')


BOT.run(credentials['Token'])
