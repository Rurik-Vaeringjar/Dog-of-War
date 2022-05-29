import discord
from discord.ext import commands

from lib.pybmapi.bm_api import bm_api
class BattleMetrics(commands.Cog):
	def __init__(self, bot, token):
		self.bot = bot
		self._last_member = None
		self.token = token

	@commands.command(name="servers", help="Get information about Merciless' HLL Servers")
	async def get_server_info(self, ctx, arg=None):
		#14757084 [Merc] US EAST
		#15120335 [Merc] US WEST

		time = 30.0
		if arg == "sticky":
			time = None

		bmapi = bm_api(self.token)
		servers = [bmapi.get_server_info(14757084), bmapi.get_server_info(15120335)]	
		embeds = []
		for server in servers:
			attr = server['data']['attributes']
			id_ = attr['id']
			name = "[MERC] - US EAST D.C" if "US EAST" in attr['name'] else "[MERC] - US WEST L.A."
			ip = attr['ip']
			players = attr['players']
			max_players = attr['maxPlayers']
			queryport = attr['portQuery']
			map = attr['details']['map']
			link = "https://www.battlemetrics.com/servers/hll/" + id_

			embed = discord.Embed(title=name, url=link)
			embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/832367939021570079/975743305138716682/unknown.png")
			embed.add_field(name="IP", value=ip, inline=True)
			if time:
				embed.add_field(name="Map", value=map, inline=True)
				embed.add_field(name="Players", value=f"{players}/{max_players}", inline=True)
			embed.add_field(name="Direct Connect Here", value=f"steam://connect/{ip}:{queryport}", inline=False)		

			await ctx.send(embed=embed, delete_after=time)
		
		if time:
			await ctx.message.delete()
		

	@commands.command(name="test", hidden=True)
	async def test_func(self, ctx):
		msg = "Test successful, cog works."
		await ctx.send(msg, delete_after=5.0)
		await ctx.message.delete()

