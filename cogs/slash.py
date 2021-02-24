import discord
from discord.ext import commands
import time
import discord_slash
from discord_slash import cog_ext

class slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="test", guild_ids=[786359602241470464])
    async def test(self, ctx, arg1, arg2):
        await ctx.send(f"{arg1} {arg2}")
    @cog_ext.cog_slash(name="ping")
    async def ping(self, ctx):
        embed = await discord.Embed(color=self.bot.color)
        embed.set_author(name="ping")
        embed.add_field(name="<:stab:744345955637395586>  websocket latency",
                        value=f"```{round(self.bot.latency * 1000)} ms ```")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(slash(bot))