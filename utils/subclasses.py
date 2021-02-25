import discord
import itertools
from discord_slash import SlashCommand
import sys
import vacefron
import ipc
import subprocess
import mystbin
import aiohttp
import psutil
import time
from collections import Counter
from asyncdagpi import Client
from utils.asyncstuff import asyncexe
import alexflipnote
import aiozaneapi
import eight_ball
import os
alex_ = os.getenv("alex_")
ipc_key=os.getenv("ipc_key")
zane_api = os.getenv("zane_api")
TOKEN_ACCESS = os.getenv("TOKEN_ACCESS")
api_token = os.getenv("api_token")
import re
from discord.ext import commands
from utils.HelpPaginator import HelpPaginator, CannotPaginate
token=re.compile(r"([a-zA-Z0-9]{24}\.[a-zA-Z0-9]{6}\.[a-zA-Z0-9_\-]{27}|mfa\.[a-zA-Z0-9_\-]{84})")
class AnimeContext(commands.Context):
  @discord.utils.cached_property
  def replied_reference(self):
      ref = self.message.reference
      if ref and isinstance(ref.resolved, discord.Message):
          return ref.resolved.to_reference()
      return None
  @asyncexe()
  def all_possible_caps_(self, text):
    return list(map(''.join, itertools.product(*((c.upper(), c.lower()) for c in text))))

  async def all_possible_caps(self, text):
    return await self.all_possible_caps_(text)
  def big_embed(self):
    embed = discord.Embed(color=0x00ff6a, title="a"*256, description="a"*2048)
    embed.add_field(name="a"*256, value="a"*112)
    embed.add_field(name="a"*256, value="a"*1024)
    embed.set_footer(text="a"*2048)
    return embed
  async def ovoly(self, msg):
    ovo = msg.replace("l", "v").replace("L", "v").replace("r", "v").replace("R", "v")
    print(self)
    return f"{ovo} ovo"
  async def get(self, link):
    try:
      return str(await self.bot.mystbin.get(link))
    except:
      return None
  async def paste(self, content):
    return str(await self.bot.mystbin.post(content))
  async def send(self, content=None, **kwargs):
    # if self.invoked_with("jishaku"):
    #   embed = discord.Embed(color=0x2ecc71, description=content)
    #   message = super().send(content=None, embed=embed)
    #   return message
    if not self.message.channel.permissions_for(self.me).text():
      return False
    if self.message.id in self.bot._message_cache:
      if self.message.edited_at:
        msg = self.bot._message_cache[self.message.id]
        if content:
            if "embed" in kwargs:
              kwargs.pop("embed")
        await msg.edit(content=content, **kwargs)
        return msg
      else:
        message = await super().send(content, **kwargs)
        return message
    else:
      message = await super().send(content, **kwargs)
      self.bot._message_cache[self.message.id] = message
      return message
  async def reply(self, content=None, **kwargs):
    if self.message.id in self.bot._message_cache:
      if self.message.edited_at:
        msg = self.bot._message_cache[self.message.id]
        if content:
            if "embed" in kwargs:
              kwargs.pop("embed")
        await msg.edit(content=content, **kwargs)
        return msg
      else:
        message = await super().send(content, **kwargs)
        return message
    else:
      message = await super().reply(content, **kwargs)
      self.bot._message_cache[self.message.id] = message
      return message
class AnimeMessage(discord.Message):
  pass
class GlobalCooldown(commands.CommandOnCooldown):
  pass
class AnimeColor(discord.Color):
    def init(self, args, **kwargs):
        super().init(args, **kwargs)

    @classmethod
    def lighter_green(cls):
        return cls(0x00ff6a)
async def prefix_get(bot, message):
  return ['OVO ', 'OVO ', 'OVo ', 'OVo ', 'OvO ', 'OvO ', 'Ovo ', 'Ovo ', 'oVO ', 'oVO ', 'oVo ', 'oVo ', 'ovO ', 'ovO ', 'ovo ', 'ovo ']

class AnimeBot(commands.AutoShardedBot):
  def __init__(self):
    intents = discord.Intents.default()
    intents.members=True
    # self.ipc = ipc.Server(self, secret_key=ipc_key)
    self.command_list = []
    super().__init__(command_prefix=prefix_get, 
max_messages=1000, 
intents=intents, 
description="""
|_   _| |__   ___     / \   _ __ (_)_ __ ___   ___  | __ )  ___ | |_ 
  | | | '_ \ / _ \   / _ \ | '_ \| | '_ ` _ \ / _ \ |  _ \ / _ \| __|
  | | | | | |  __/  / ___ \| | | | | | | | | |  __/ | |_) | (_) | |_ 
  |_| |_| |_|\___| /_/   \_\_| |_|_|_| |_| |_|\___| |____/ \___/ \__|
""",
chunk_guilds_at_startup=False, 
case_insensitive=True, allowed_mentions=discord.AllowedMentions(everyone=False, replied_user=False))
  def run(self, *args, **kwargs):
    # self.ipc.start()
    subprocess.check_output("pip install speedtest-cli", shell=True)
    self.deleted_message_cache = {}
    self.concurrency = []
    self.color = 0x00ff6a
    self.psutil_process = psutil.Process()
    self._message_cache = {} 
    self.prefixes = {}
    self.socket_receive = 0
    self.start_time = time.time()
    self.socket_stats = Counter()
    self.command_counter = 0
    self.commandsusages = Counter()
    self.session = aiohttp.ClientSession(headers={"User-Agent": f"python-requests/2.20.0 The Anime Bot/1.1.0 Python/{sys.version_info[0]}.{sys.version_info[1]}.{sys.version_info[2]} aiohttp/{aiohttp.__version__}"})
    self.mystbin = mystbin.Client(session=self.session)
    self.vacefron_api=vacefron.Client(session=self.session, loop=self.loop)
    self.dag = Client(api_token, session=self.session, loop=self.loop)
    self.alex=alexflipnote.Client(alex_, session=self.session, loop=self.loop)
    self.ball = eight_ball.ball()
    self.zaneapi = aiozaneapi.Client(zane_api)
    for command in self.commands:
      self.command_list.append(str(command))
      self.command_list.extend([alias for alias in command.aliases])
      if isinstance(command, commands.Group):
          for subcommand in command.commands:
              self.command_list.append(str(subcommand))
              self.command_list.extend([f"{command} {subcommand_alias}" for subcommand_alias in subcommand.aliases])
              if isinstance(subcommand, commands.Group):
                  for subcommand2 in subcommand.commands:
                      self.command_list.append(str(subcommand2))
                      self.command_list.extend([f"{subcommand} {subcommand2_alias}" for subcommand2_alias in subcommand2.aliases])
                      if isinstance(subcommand2, commands.Group):
                          for subcommand3 in subcommand2.commands:
                              self.command_list.append(str(subcommand3))
                              self.command_list.extend([f"{subcommand2} {subcommand3_alias}" for subcommand3_alias in subcommand3.aliases])
    super().run(*args, **kwargs)
  def get_message(self, message_id):
    return self._connection._get_message(message_id)

  async def get_context(self, message, *, cls=AnimeContext):
    return await super().get_context(message, cls=cls)
  async def is_ratelimited(self):
    result = await self.is_ws_ratelimited()
    return result

  