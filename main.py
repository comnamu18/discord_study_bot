import os

from discord.ext import commands
from dotenv import load_dotenv

from utils import handle_time_orm
from utils import handle_db_orm_sqlite

from utils.handle_db import *
from utils.handle_time import *


load_dotenv()
token = os.getenv("DISCORD_TOKEN")
db_name = os.getenv("DISCORD_DB")
tb_name = os.getenv("DISCORD_DB_TB")
admin_name = os.getenv("DISCORD_ADMIN")

bot = commands.Bot(command_prefix="!")

db_handler = handle_db_orm_sqlite.DB_Handler(db_name)


@bot.event
async def on_ready():
    init_db(db_name, tb_name)
    print(f"{bot.user.name} has connected to Discord!")


@bot.command(name="orm_alluser")
async def sql(ctx):
    results = db_handler.get_all_users()
    result = ""
    for i in results:
        result += str(i) + "\n"

    await ctx.send(result)


@bot.command(name="orm_me")
async def sql2(ctx):
    current_time = handle_time_orm.get_current_time_object()
    user = db_handler.start_study(ctx.author.name, current_time)
    await ctx.send(str(user))


@bot.command(name="orm_hi")
async def hi1(ctx):
    current_time = handle_time_orm.get_current_time_object()
    db_handler.start_study(ctx.author.name, current_time)
    await ctx.send(f"{current_time} : 안녕하세요 {ctx.author.name}님!")


@bot.command(name="orm_bye")
async def bye1(ctx):
    current_time = handle_time_orm.get_current_time_object()
    db_handler.end_study(ctx.author.name, current_time)
    await ctx.send(f"{current_time} :안녕히가세요 {ctx.author.name}님!")


@bot.command(name="hi")
async def hi(ctx):
    current_time = get_current_time()
    start_study(ctx.author.name, tb_name, current_time)
    await ctx.send(f"{current_time} : 안녕하세요 {ctx.author.name}님!")


@bot.command(name="bye")
async def bye(ctx):
    current_time = get_current_time()
    end_study(ctx.author.name, tb_name, current_time)
    await ctx.send(f"{current_time} :안녕히가세요 {ctx.author.name}님!")


@bot.command(name="list")
async def listing(ctx):
    list_all_from_db = list_study(tb_name)
    await ctx.send(list_all_from_db)


@bot.command(name="exit")
async def exitBot(ctx):
    if ctx.author.name == admin_name:
        close_db()
        print("Close the bot")
        return
    else:
        await ctx.send("Admin만 이 명령어를 사용할 수 있습니다.")


@bot.event
async def on_error(event, *args, **kwargs):
    with open("err.log", "a") as f:
        if event == "on_message":
            f.write(f"Unhandled message: {args[0]}\n")
        else:
            raise


bot.run(token)
