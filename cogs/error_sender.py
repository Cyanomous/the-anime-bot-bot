import aiohttp
import discord
import os
webhook_url = os.getenv("webhook")
from discord import AsyncWebhookAdapter, Webhook
from discord.ext import commands


class error_sender(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        if not ctx.guild:
            server = "DM "
            name = ctx.author
        else:
            server = "Server"
            name = ctx.guild.name
        fields = [["Error", error], ["Author", ctx.author], [server, name],
                  ["Message", ctx.message.content]]
        embed = discord.Embed(color=0xFF0000, title="An error occured")
        [
            embed.add_field(name=f"**{n}**",
                            value=f"```py\n{v}```",
                            inline=False) for n, v in fields
        ]
        webhook = Webhook.from_url(
            webhook_url,
            adapter=AsyncWebhookAdapter(self.bot.session))
        return await webhook.send(embed=embed)


def setup(bot):
    bot.add_cog(error_sender(bot))
