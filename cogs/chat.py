import discord
from discord.ext import commands
from matplotlib import pyplot as plt
from utils.asyncstuff import asyncexe
from collections import Counter
import numpy as np

class chat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @staticmethod
    @asyncexe()
    def graph_(msg):
        author = []
        count = []
        for i, (n,v) in enumerate(msg.most_common()):
            author.append(n)
            count.append(v)
        patches, texts = plt.pie(count, labels = author) 
        plt.legend(patches, author, loc="best")
        plt.axis('equal')
        plt.tight_layout()
        plt.savefig("chatgraph.png")
        return
    @commands.command()
    async def chatgraph(self, ctx, *, limit:int=500):
        if limit > 10000:
            limit = 10000
        await ctx.send("Collecting might take long")
        msg = Counter()
        async for message in ctx.channel.history(limit = limit):
            if message.author.bot == True:
                continue
            msg[message.author.name] += 1
        await self.graph_(msg)
        await ctx.send(file=discord.File("chatgraph.png"))
def setup(bot):
    bot.add_cog(chat(bot))