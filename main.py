import os

from discord.ext import commands
from dotenv import load_dotenv
from utils import handle_db
from utils import handle_time

from msgs.db_msg import db_msgs

load_dotenv()
token = os.getenv("DISCORD_TOKEN")
db_name = os.getenv("DISCORD_DB")
admin_name = os.getenv("DISCORD_ADMIN")

bot = commands.Bot(command_prefix="!")

db_handler = handle_db.DbHandler(db_name)


@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")


@bot.command(name="hi")
async def hi(ctx):
    current_time = handle_time.get_current_time()
    hi_result = db_handler.start_study(ctx.author, current_time)
    result_msg = db_msgs.get(hi_result).format(time=current_time, name=ctx.author.name)
    await ctx.send(result_msg)


@bot.command(name="bye")
async def bye(ctx):
    current_time = handle_time.get_current_time()
    bye_result = db_handler.end_study(ctx.author, current_time)
    result_msg = db_msgs.get(bye_result).format(time=current_time, name=ctx.author.name)
    await ctx.send(result_msg)


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
    user_id = ctx.author.id
    study_logs = db_handler.get_my_study_logs(user_id)
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
