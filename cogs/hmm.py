import discord
from discord.ext import commands
import copy
import datetime


class reactionrole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.role_message_id = 812122122968367124
        self.emoji_to_role = {
            "\U0001f33b": 812116205540081714,
            "\U0001f339": 812116259012476959,
            "\U0001f33c": 812116231737966622
        }

    def cog_check(self, ctx):
        if not ctx.guild:
            return False
        elif not ctx.guild.id == 701251070977900584:
            return False
        else:
            return True

    # @commands.Cog.listener()
    # async def on_raw_message_delete(self, payload):
    #     if payload.guild_id == 701251070977900584:
    #         msg = self.bot.deleted_message_cache.get(payload.message_id)
    #         if not msg:
    #             return
    #         embed = discord.Embed(color=self.bot.color)
    #         embed.set_author(name=msg.author.display_name,
    #                          icon_url=str(msg.author.avatar_url))
    #         embed.add_field(name="Message delete",
    #                         value=f"Message: {msg.content}")
    #         await self.bot.get_channel(812054734919303189).send(embed=embed)
    #         self.bot.deleted_message_cache.pop(payload.message_id)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        """Gives a role based on a reaction emoji."""
        # Make sure that the message the user is reacting to is the one we care about
        if payload.message_id != self.role_message_id:
            return

        try:
            role_id = self.emoji_to_role[payload.emoji.id
                                         or payload.emoji.name]
        except KeyError:
            # If the emoji isn't the one we care about then exit as well.
            return

        guild = self.bot.get_guild(payload.guild_id)
        if guild is None:
            # Check if we're still in the guild and it's cached.
            return

        role = guild.get_role(role_id)
        if role is None:
            # Make sure the role still exists and is valid.
            return

        try:
            # Finally add the role
            await payload.member.add_roles(role)
        except discord.HTTPException:
            # If we want to do something in case of errors we'd do it here.
            pass

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        """Removes a role based on a reaction emoji."""
        # Make sure that the message the user is reacting to is the one we care about
        if payload.message_id != self.role_message_id:
            return

        try:
            role_id = self.emoji_to_role[payload.emoji.id
                                         or payload.emoji.name]
        except KeyError:
            # If the emoji isn't the one we care about then exit as well.
            return

        guild = self.bot.get_guild(payload.guild_id)
        if guild is None:
            # Check if we're still in the guild and it's cached.
            return

        role = guild.get_role(role_id)
        if role is None:
            # Make sure the role still exists and is valid.
            return

        member = guild.get_member(payload.user_id)
        if member is None:
            # Makes sure the member still exists and is valid
            return

        try:
            # Finally, remove the role
            await member.remove_roles(role)
        except discord.HTTPException:
            # If we want to do something in case of errors we'd do it here.
            pass


def setup(bot):
    bot.add_cog(reactionrole(bot))
