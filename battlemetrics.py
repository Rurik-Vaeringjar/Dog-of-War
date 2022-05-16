import discord
from discord.ext import commands

from lib.pybmapi.bm_api import bm_api
class BattleMetrics(commands.Cog):
	def __init__(self, bot, token):
		self.bot = bot
		self._last_member = None
		self.token = token

	@commands.command(name="servers", hidden=True)
	async def get_server_info(self, ctx):
		#14757084 [Merc] US EAST
		#15120335 [Merc] US WEST
		bmapi = bm_api(self.token)
		servers = [bmapi.get_server_info(14757084), bmapi.get_server_info(15120335)]	
		for server in servers:
			await ctx.send(server)
		

	@commands.command(name="test", hidden=True)
	async def test_func(self, ctx):
		msg = "Test successful, cog works."
		await ctx.send(msg)

