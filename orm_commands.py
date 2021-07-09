import os

from utils import handle_time_orm
from utils import handle_db_orm

from dotenv import load_dotenv

load_dotenv()
sqlite_db = os.getenv("DISCORD_DB_SQLITE")
mysql_db = os.getenv("DISCORD_DB_MYSQL")


def add_sqlite_orm_commands(bot):
    sqlite_db_handler = handle_db_orm.DB_Handler(sqlite_db)

    @bot.command(name="sqlite_create")
    async def sqlite_create(ctx):
        sqlite_db_handler.create_user_table()
        await ctx.send("good")

    @bot.command(name="sqlite_alluser")
    async def sqlite_alluser(ctx):
        results = sqlite_db_handler.get_all_users()
        result = ""
        for i in results:
            result += str(i) + "\n"

        if result == "":
            result = "empty"
        await ctx.send(result)

    @bot.command(name="sqlite_me")
    async def sqlite_me(ctx):
        current_time = handle_time_orm.get_current_time_object()
        user = sqlite_db_handler.get_user_object_by_user_name(ctx.author.name)
        await ctx.send(str(user))

    @bot.command(name="sqlite_hi")
    async def sqlite_hi(ctx):
        current_time = handle_time_orm.get_current_time_object()
        sqlite_db_handler.start_study(ctx.author.name, current_time)
        await ctx.send(f"{current_time} : 안녕하세요 {ctx.author.name}님!")

    @bot.command(name="sqlite_bye")
    async def sqlite_bye(ctx):
        current_time = handle_time_orm.get_current_time_object()
        sqlite_db_handler.end_study(ctx.author.name, current_time)
        await ctx.send(f"{current_time} :안녕히가세요 {ctx.author.name}님!")


def add_mysql_orm_commands(bot):
    mysql_db_handler = handle_db_orm.DB_Handler(mysql_db)

    @bot.command(name="mysql_create")
    async def mysql_create(ctx):
        mysql_db_handler.create_user_table()
        await ctx.send("good")

    @bot.command(name="mysql_alluser")
    async def mysql_alluser(ctx):
        results = mysql_db_handler.get_all_users()
        result = ""
        for i in results:
            result += str(i) + "\n"

        if result == "":
            result = "empty"
        await ctx.send(result)

    @bot.command(name="mysql_me")
    async def mysql_me(ctx):
        current_time = handle_time_orm.get_current_time_object()
        user = mysql_db_handler.get_user_object_by_user_name(ctx.author.name)
        await ctx.send(str(user))

    @bot.command(name="mysql_hi")
    async def mysql_hi(ctx):
        current_time = handle_time_orm.get_current_time_object()
        mysql_db_handler.start_study(ctx.author.name, current_time)
        await ctx.send(f"{current_time} : 안녕하세요 {ctx.author.name}님!")

    @bot.command(name="mysql_bye")
    async def mysql_bye(ctx):
        current_time = handle_time_orm.get_current_time_object()
        mysql_db_handler.end_study(ctx.author.name, current_time)
        await ctx.send(f"{current_time} :안녕히가세요 {ctx.author.name}님!")
