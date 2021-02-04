import os
from datetime import datetime 

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='hi')
async def hi(ctx):
    await ctx.send(f'안녕하세요 {ctx.author.name}님!')
    
@bot.command(name='bye')
async def bye(ctx):
    await ctx.send(f'안녕히가세요 {ctx.author.name}님!')

@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise

bot.run(TOKEN)