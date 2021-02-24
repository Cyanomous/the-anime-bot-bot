from collections import Counter

import discord
from discord.ext import commands

from jishaku.paginators import PaginatorInterface, PaginatorEmbedInterface


class commandsusage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        self.bot.command_counter += 1
        self.bot.commandsusages[ctx.command.qualified_name] += 1

    @commands.command()
    async def commandsusage(self, ctx):
        counter = 0
        lists = []
        lists.append(f"Total {self.bot.command_counter} commands invoked")
        for i, (n, v) in enumerate(self.bot.commandsusages.most_common()):
            counter += 1
            lists.append(f"`{counter}. {n:<10} {v}`")
        paginator = commands.Paginator(max_size=1800,
                                        prefix="",
                                        suffix="")
        for i in lists:
            paginator.add_line(i)
        interface = PaginatorEmbedInterface(ctx.bot,
                                        paginator,
                                        owner=ctx.author)
        return await interface.send_to(ctx)

def setup(bot):
    bot.add_cog(commandsusage(bot))
