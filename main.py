import os

from discord.ext import commands
from dotenv import load_dotenv
from utils import handle_db
from utils import handle_time

load_dotenv()
token = os.getenv("DISCORD_TOKEN")
db_name = os.getenv("DISCORD_DB")
tb_name = os.getenv("DISCORD_DB_TB")
admin_name = os.getenv("DISCORD_ADMIN")

bot = commands.Bot(command_prefix="!")

db_handler = handle_db.DbHandler(db_name)


@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")


@bot.command(name="hi")
async def hi(ctx):
    current_time = handle_time.get_current_time()
    db_handler.start_study(ctx.author.name, current_time)
    await ctx.send(f"{current_time} : 안녕하세요 {ctx.author.name}님!")


@bot.command(name="bye")
async def bye(ctx):
    current_time = handle_time.get_current_time()
    db_handler.end_study(ctx.author.name, current_time)
    await ctx.send(f"{current_time} :안녕히가세요 {ctx.author.name}님!")


@bot.command(name="alluser")
async def alluser(ctx):
    all_users = db_handler.get_all_users()
    all_users_text = ""
    for x in all_users:
        all_users_text += str(x) + "\n"

    if all_users_text == "":
        all_users_text = "empty"
    await ctx.send(all_users_text)


@bot.command(name="mylog")
async def mylog(ctx):
    user_name = ctx.author.name
    study_logs = db_handler.get_all_study_logs(user_name)
    study_logs_text = ""
    for x in study_logs:
        study_logs_text += str(x) + "\n"

    if study_logs_text == "":
        study_logs_text = "공부 기록이 없네요"
    await ctx.send(study_logs_text)


@bot.command(name="exit")
async def exitBot(ctx):
    if ctx.author.name == admin_name:
        del db_handler
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
