import discord
from discord.ext import commands

class utils:
    async def get_pic(self, ctx):
        msg = ctx.message
        if not msg.reference:
            return False
        if msg.reference.cached_message:
            if msg.reference.cached_message.attachments:
                return msg.reference.cached_message.attachments.url
            if msg.reference.cached_message.embeds.url:
                return msg.reference.cached_message.embeds.url
        else:
            if msg.reference.cached_message.message_id and msg.reference.cached_message.channel_id:
                msg = await ctx.bot.get_channel(msg.channel_id).fetch_message(msg.message.id)
                if msg.attachments:
                    return msg.reference.cached_message.attachments.url
                if msg.embeds.url:
                    return msg.reference.cached_message.embeds.url

        return False