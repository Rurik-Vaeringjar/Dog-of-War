#bot.py

import os
from dotenv import load_dotenv

import discord
from discord.ext import commands

from tools.useful_functions import log, log_nl

load_dotenv()
TOKEN = os.getenv("TOKEN")

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
async def on_message(message):
	if message.author == bot.user:
		return
	
	if message.channel.name == "new-members-tag-assignment":
		await rolecaller(message)
		
	if message.channel.name == "hll-admin-log" and message.author.name == "Hook of War":
		await modify_webhook(message)

	#REACTION TESTING
	#if message.channel.name == 'bot-spam':
		#await message.add_reaction("\U0001f44d")
		#log(f"UPD: Reacted to message in bot-spam")

	await bot.process_commands(message)

async def rolecaller(message):
	rolegiven = False
	msg = message.content
	msg = msg.lower()

	if "hll" in msg or "hell let loose" in msg:
		role = discord.utils.get(message.guild.roles, name="Hll")
		await message.author.add_roles(role)
		await message.add_reaction("<:hll:969397971865182218>")
		log(f"UPD: {message.author} given {role}")

	if "tbc" in msg or "wow" in msg or "world of warcraft" in msg:
		role = discord.utils.get(message.guild.roles, name="World of Warcraft")
		await message.author.add_roles(role)
		await message.add_reaction("<:wow:969397993675554856>")
		log(f"UPD: {message.author} given {role}")

	if "lost ark" in msg or msg.startswith("ark") or " ark " in msg:
		role = discord.utils.get(message.guild.roles, name="Lost Ark")
		await message.author.add_roles(role)
		await message.add_reaction("<:ark:969401546565615717>")
		log(f"UPD: {message.author} given {role}")

	if "new world" in msg:
		role = discord.utils.get(message.guild.roles, name="New World")
		await message.author.add_roles(role)
		rolegiven = True
		log(f"UPD: {message.author} given {role}")

	if "valheim" in msg or "valhiem" in msg:
		role = discord.utils.get(message.guild.roles, name="Valheim")
		await message.author.add_roles(role)
		rolegiven = True
		log(f"UPD: {message.author} given {role}")

	if "arma" in msg:
		role = discord.utils.get(message.guild.roles, name="Arma 3")
		await message.author.add_roles(role)
		rolegiven = True
		log(f"UPD: {message.author} given {role}")

	if "foxhole" in msg:
		role = discord.utils.get(message.guild.roles, name="FoxHole")
		await message.author.add_roles(role)
		rolegiven = True
		log(f"UPD: {message.author} given {role}")

	if rolegiven:
		await message.add_reaction("\U0001f44d")

	if "admin" in msg:
		if "jk" in msg:
			return
		if "please" not in msg:
			await message.reply("Ah ah ah, you didn't say the magic word!", mention_author=False)
		else:
			await message.reply("No.", mention_author=False)

async def modify_webhook(message):
	msg = message.content

	msg = msg.replace("[MERC] -US WEST L.A Discord.GG/m3rc", "```ini\n[US WEST]")
	msg = msg.replace("[MERC] - US EAST D.C. Discord.GG/m3rc", "```css\n[US EAST]")
	msg += "\n```"

	await message.channel.send(msg)
	await message.delete()
	
	msg = msg.replace("```ini\n", "")
	msg = msg.replace("```css\n", "")
	msg = msg.replace("\n```", "")

	log(f"LOG: {msg}")


bot.run(TOKEN)
