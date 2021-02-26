import discord
from discord.ext import commands
import copy
import datetime


class reactionrole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.role_message_id = 812050921714089996
        self.emoji_to_role = {
            701518910842732640: 701546882320826428,
            711089394031001600: 701543891119243324,
            658157341816127498: 701906891848024124,
            800088795281227828: 810336158008737792,
            "\U0001f9a2": 812052162782691338,
            800088141955858463: 812054058651091016,
            800088641267433493: 812054326871719976,
            800088680009957387: 812054426831290440,
            "\U0001f33f": 812058367739691028,
            800088726923116574: 812054545035165706,
            "\U0001f38d": 812058367098748929,
            690260332911919140: 812058368503840819,
            "\U0001fad0": 812058362028097606,
            798949801630236702: 812057014888955935,
            699503385824722964: 812058366360027146,
            798949802322427955: 812057852550185041,
            694419633150885909: 812058369279787018,
            800088895722225685: 812058369807876166,
            691499259438170152: 811804360107360267
        }

    def cog_check(self, ctx):
        return bool(ctx.guild and ctx.guild.id == 701251070977900584)

    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload):
        if payload.guild_id == 701251070977900584:
            msg = self.bot.deleted_message_cache.get(payload.message_id)
            if not msg:
                return
            embed = discord.Embed(color=self.bot.color)
            embed.set_author(name=msg.author.display_name,
                             icon_url=str(msg.author.avatar_url))
            embed.add_field(name="Message delete",
                            value=f"Message: {msg.content}")
            await self.bot.get_channel(812054734919303189).send(embed=embed)
            self.bot.deleted_message_cache.pop(payload.message_id)

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
