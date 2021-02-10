import os
from datetime import datetime, timedelta 

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
    current_time = datetime.now().strftime("%Y년%m월%d일 %H시%M분%S초")
    current_time = current_time + timedelta(seconds=120)
    send_message = f'안녕하세요 name:{ctx.author.name}님! : {current_time}'
    await ctx.send(send_message)
    
@bot.command(name='bye')
async def bye(ctx):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    current_time = current_time + timedelta(seconds=120)
    send_message = f'안녕히가세요 name:{ctx.author.name}님! : {current_time}'
    await ctx.send(send_message)

@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')

bot.run(TOKEN)