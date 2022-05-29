#bot.py

import os
from dotenv import load_dotenv

import discord
from discord.ext import commands

from tools.useful_functions import log, log_nl

from merc import Merciless
from battlemetrics import BattleMetrics


load_dotenv()
TOKEN = os.getenv("TOKEN")
BMTOKEN = os.getenv("BMTOKEN")

intents = discord.Intents.default()
intents.members = True
cmd = '.'
bot = commands.Bot(command_prefix=cmd, intents=intents)

startup = True

################################################################################################################### EVENTS
@bot.event
async def on_ready():
	global startup
	if startup:
		for guild in bot.guilds:
			if guild:
				log(f"SRV: {bot.user} has connected to {guild.name} (id: {guild.id})")
		startup = False

@bot.event
async def on_connect():
	if startup:
		log(f"NET: {bot.user} has connected to Discord")

@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.CommandNotFound):
		return
	raise error

@bot.event
async def on_message(message):
	if message.author == bot.user:
		return

	#delete = False
	msg = message.content 
	#if msg == f"{cmd}servers" or msg.startswith(f"{cmd}nicknuke") or msg.startswith(f"{cmd}clearnicknuke"):
	#	delete = True

	#REACTION TESTING
	#if message.channel.name == 'bot-spam':
		#await message.add_reaction("\U0001f44d")
		#log(f"UPD: Reacted to message in bot-spam")

	try:
		await bot.process_commands(message)
	except:
		log("ERR: Something went wrong with process_commands")

	#if delete:
	#	await message.delete()


bot.add_cog(Merciless(bot))
bot.add_cog(BattleMetrics(bot, BMTOKEN))

bot.run(TOKEN)
