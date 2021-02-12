import os
from datetime import datetime, timedelta 

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')
user_dict = {}

def get_current_time():
    current_time = datetime.now() + timedelta(seconds=120)
    return current_time.strftime("%Y-%m-%d %H:%M:%S")

def calculate_elpased(start_time, end_time):
    start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")

    return end_time - start_time

def handle_timedelta(td):
    days = td.days
    hours = td.seconds//3600
    minutes = (td.seconds//60)%60
    seconds = td.seconds % 60
    return_string = ''
    if days != 0:
        return_string += f'{days}일 '
    if hours != 0:
        return_string += f'{hours}시간 '
    if minutes != 0:
        return_string += f'{minutes}분 '
    if seconds != 0:
        return_string += f'{seconds}초'

    return return_string

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='hi')
async def hi(ctx):
    user_name = ctx.author.name
    current_time = get_current_time()

    if user_name not in user_dict:
        user_dict[user_name] = {"start_time":None, "count":0, "elapsed_time":timedelta(0)}
    user_dict[user_name]["start_time"] = current_time

    send_message = f'안녕하세요 {user_name}님! : {current_time}'
    await ctx.send(send_message)
    
@bot.command(name='bye')
async def bye(ctx):
    user_name = ctx.author.name
    current_time = get_current_time()
    
    if user_name in user_dict:
        if user_dict[user_name]["start_time"] is not None:
            user_dict[user_name]["elapsed_time"] += calculate_elpased(user_dict[user_name]["start_time"],
                                                                      current_time)
            user_dict[user_name]["count"] += 1
            user_dict[user_name]["start_time"] = None

    send_message = f'수고하셨습니다 {user_name}님! : {current_time}'
    await ctx.send(send_message)

@bot.command(name='list')
async def listing_results(ctx):
    send_message = '총 공부 시간 리스트 (정렬X)\n'
    for user_name, study_record in user_dict.items():
        elapsed_time = handle_timedelta(study_record["elapsed_time"])
        send_message += f'{user_name} : 총 시간 {elapsed_time}, {study_record["count"]}회 진행\n'
    
    await ctx.send(send_message)

@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')

bot.run(TOKEN)
