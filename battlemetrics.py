import discord
from discord.ext import commands

class BattleMetrics(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self._last_member = None

	@commands.command(name="test", hidden=True)
	async def test_func(self, ctx):
		msg = "Test successful, cog works."
		await ctx.send(msg)

