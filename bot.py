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
	
	#new-members-tag-assignment
	if message.channel.id == 834565569180991488: 
		await rolecaller(message)
		
	#hll-admin-log
	if message.channel.id == 968889649428848650 and message.author.name == "Hook of War":
		await modify_log_webhook(message)

	#hll-admin-ping
	if message.channel.id == 968984419828375662 and message.author.name == "Hook of War":
		await modify_help_webhook(message)

	#REACTION TESTING
	#if message.channel.name == 'bot-spam':
		#await message.add_reaction("\U0001f44d")
		#log(f"UPD: Reacted to message in bot-spam")

	await bot.process_commands(message)

#-------------------------------------------------------------------------------------------------------- rolecaller
async def rolecaller(message):
	rolegiven = False
	msg = message.content
	msg = msg.lower()

	if "hll" in msg or "hell let loose" in msg:
		if (await give_role(message, 820820382197743639)):
			await message.add_reaction("<:hll:969397971865182218>")

	if "tbc" in msg or "wow" in msg or "world of warcraft" in msg:
		if (await give_role(message, 965436847616589885)):
			await message.add_reaction("<:wow:969397993675554856>")

	if "lost ark" in msg or msg.startswith("ark") or " ark " in msg or " ark," in msg:
		if (await give_role(message, 822006223099396156)):
			await message.add_reaction("<:ark:969401546565615717>")

	if "new world" in msg:
		if (await give_role(message, 844697336595742721)):
			rolegiven = True

	if "valheim" in msg or "valhiem" in msg:
		if (await give_role(message, 757176232801468477)):
			rolegiven = True

	if "arma" in msg:
		if (await give_role(message, 823332560087679007)):
			rolegiven = True

	if "foxhole" in msg:
		if(await give_role(message, 693723031482269766)):
			rolegiven = True
		
	if rolegiven:
		await message.add_reaction("\U0001f44d")

	if "admin" in msg:
		if "jk" in msg:
			return
		if "please" not in msg:
			await message.reply("Ah ah ah, you didn't say the magic word!", mention_author=False)
		else:
			await message.reply("No.", mention_author=False)

async def give_role(message, id) -> bool:
	role = discord.utils.get(message.guild.roles, id=id)
	if role and role not in message.author.roles:
		await message.author.add_roles(role)
		log(f"UPD: {message.author} given {role}")
		return True
	return False



#-------------------------------------------------------------------------------------------------------- modify_log_webhook
async def modify_log_webhook(message):
	msg = message.content

	msg = msg.replace("[MERC] -US WEST L.A Discord.GG/m3rc", "```ini\n[US WEST]")
	msg = msg.replace("[MERC] - US EAST D.C. Discord.GG/m3rc", "```css\n[US EAST]")
	msg += "\n```"
	
	try:
		await message.channel.send(msg)
	except:
		log(f"ERR: Failed to format webhook, aborting delete.")
	else:
		await message.delete()
	
	msg = msg.replace("```ini\n", "")
	msg = msg.replace("```css\n", "")
	msg = msg.replace("\n```", "")

	log(f"LOG: {msg}")

#-------------------------------------------------------------------------------------------------------- modify_help_webhook
async def modify_help_webhook(message):
	msg = message.content

	if ", -JesusUncuT-:" in msg:
		await message.delete()
		return
	elif ", Compton:" in msg:
		await message.delete()
		return
	elif ", cidi:" in msg:
		await message.delete()
		return

	msg = msg.replace("[MERC] -US WEST L.A Discord.GG/m3rc", "US WEST")
	msg = msg.replace("[MERC] - US EAST D.C. Discord.GG/m3rc", "US EAST")
	msg = msg.replace("!adminhelp", "")
	msg = msg.replace("!ADMINHELP", "")	
	msg = msg.replace("!admin", "")

	msg = "<@&693723013459476491> " + msg

	try:
		await message.channel.send(msg)
	except:
		log(f"ERR: Failed to format webhook, aborting delete.")
	else:
		await message.delete()

	log(f"LOG: {msg}")

bot.run(TOKEN)
