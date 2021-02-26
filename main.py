import asyncio
import difflib
import functools
import logging
import os
import re
import sys
import traceback
import warnings

import aioredis
import uvloop

import discord
from discord.ext import commands
from discord_slash import SlashCommand
from utils.HelpPaginator import CannotPaginate, HelpPaginator
from utils.subclasses import AnimeBot

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

warnings.filterwarnings("ignore", category=DeprecationWarning)
os.system("python3 webserver.py &")
os.system("python3 hmm.py &")
TOKEN = os.getenv("TOKEN")


bot = AnimeBot()
slash = SlashCommand(bot, sync_commands=True,
                     sync_on_cog_reload=True, override_type=True)


@slash.slash(name="wtf", guild_ids=[786359602241470464])
async def wtf(ctx):
    await ctx.respond()
    await ctx.send("wtf wtf")


os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"


bot.remove_command("help")


@bot.command(name="help")
async def _help(ctx, *, command: str = None):
    """Shows help about a command or the bot"""
    try:
        if command is None:
            p = await HelpPaginator.from_bot(ctx)
        else:
            entity = bot.get_cog(command) or bot.get_command(command)

            if entity is None:
                clean = command.replace('@', '@\u200b')
                failed_command = re.match(f"^({ctx.prefix})\s*(.*)",
                                          f"ovo {clean}",
                                          flags=re.IGNORECASE).group(2)
                matches = difflib.get_close_matches(failed_command,
                                                    ctx.bot.command_list)
                if not matches:
                    return
                return await ctx.send(
                    f"Command or category '{clean}' not found. Did you mean `{matches[0]}`?"
                )
            elif isinstance(entity, commands.Command):
                p = await HelpPaginator.from_command(ctx, entity)
            else:
                p = await HelpPaginator.from_cog(ctx, entity)

        await p.paginate()
    except Exception as error:
        print('Ignoring exception in command {}:'.format(ctx.command),
              file=sys.stderr)
        traceback.print_exception(type(error),
                                  error,
                                  error.__traceback__,
                                  file=sys.stderr)
        await ctx.send(error)


for file in os.listdir("./cogs"):
    if file.endswith(".py"):
        bot.load_extension(f"cogs.{file[:-3]}")

bot.run(TOKEN)
