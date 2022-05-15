import discord
from discord.ext import commands

from tools.useful_functions import log

class Merciless(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self._last_member = None

	@commands.Cog.listener()
	async def on_message(self, message):
		#role-request
		if message.channel.id == 834565569180991488: 
			await self.rolecaller(message)
		
		#hll-admin-log
		if message.channel.id == 968889649428848650 and message.author.name == "Hook of War":
			await self.modify_log_webhook(message)

		#hll-admin-ping
		if message.channel.id == 968984419828375662 and message.author.name == "Hook of War":
			await self.modify_help_webhook(message)

	#-------------------------------------------------------------------------------------------------------- rolecaller
	async def rolecaller(self, message):
		rolegiven = False
		msg = message.content
		msg = msg.lower()

		#role given: "Hll"
		if "hll" in msg or "hell let loose" in msg:
			if (await self.give_role(message, 820820382197743639)):
				await message.add_reaction("<:hll:969397971865182218>")

		#role given: "Squad"
		if "squad" in msg:
			if (await self.give_role(message, 834881859770384395)):
				await message.add_reaction("<:squad:975121515513274418>")

		#role given: "World of Warcraft"
		if "tbc" in msg or "wow" in msg or "world of warcraft" in msg:
			if (await self.give_role(message, 965436847616589885)):
				await message.add_reaction("<:wow:969397993675554856>")

		#role given: "Lost Ark"
		if "lost ark" in msg or msg.startswith("ark") or " ark " in msg or " ark," in msg:
			if (await self.give_role(message, 822006223099396156)):
				await message.add_reaction("<:ark:969401546565615717>")

		#role given: "New World" (gives the yellow one, check if that is the right role later)
		if "new world" in msg:
			if (await self.give_role(message, 844697336595742721)):
				rolegiven = True

		#role given: "Valheim"
		if "valheim" in msg or "valhiem" in msg:
			if (await self.give_role(message, 757176232801468477)):
				rolegiven = True

		#role given: "Arma 3"
		if "arma" in msg:
			if (await self.give_role(message, 823332560087679007)):
				rolegiven = True

		#role given: "FoxHole"
		if "foxhole" in msg:
			if(await self.give_role(message, 693723031482269766)):
				rolegiven = True

		#Thumbs up if role specific reaction not available
		if rolegiven:
			await message.add_reaction("\U0001f44d")

		#Joke post if someone requests admin
		if "admin" in msg:
			if "jk" in msg:
				return
			if "please" not in msg:
				await message.reply("Ah ah ah, you didn't say the magic word!", mention_author=False)
			else:
				await message.reply("No.", mention_author=False)

	async def give_role(self, message, id) -> bool:
		role = discord.utils.get(message.guild.roles, id=id)
		if role and role not in message.author.roles:
			await message.author.add_roles(role)
			log(f"UPD: {message.author} given {role}")
			return True
		return False#-------------------------------------------------------------------------------------------------------- modify_log_webhook

	async def modify_log_webhook(self, message):
		msg = message.content

		#Formats the server name and adds coloration via code blocks
		msg = msg.replace("[MERC] -US WEST L.A Discord.GG/m3rc", "```ini\n[US WEST]")
		msg = msg.replace("[MERC] - US EAST D.C. Discord.GG/m3rc", "```css\n[US EAST]")
		msg += "\n```"
		
		try:
			await message.channel.send(msg)
		except:
			log(f"ERR: Failed to format webhook, aborting delete.")
		else:
			await message.delete()
		
		#removes code block coloration for logging
		msg = msg.replace("```ini\n", "")
		msg = msg.replace("```css\n", "")
		msg = msg.replace("\n```", "")

		log(f"LOG: {msg}")

	#-------------------------------------------------------------------------------------------------------- modify_help_webhook
	async def modify_help_webhook(self, message):
		msg = message.content

		#deletes !admin pings from admins
		admin_list = ["Compton", "cidi", "JesusUncuT", "-JesusUncuT-", "Ruri", "cHoPsTiX"]
		for admin in admin_list:
			if f"{admin}:" in msg:
				await message.delete()
				return

		#formats the incoming ping, removing uneccessary information
		msg = msg.replace("[MERC] -US WEST L.A Discord.GG/m3rc", "US WEST")
		msg = msg.replace("[MERC] - US EAST D.C. Discord.GG/m3rc", "US EAST")
		msg = msg.replace("!adminhelp", "")
		msg = msg.replace("!ADMINHELP", "")	
		msg = msg.replace("!admin", "")

		msg_with_mention = "<@&693723013459476491> " + msg

		try:
			await message.channel.send(msg_with_mention)
		except:
			log(f"ERR: Failed to format webhook, aborting delete.")
		else:
			await message.delete()

		log(f"LOG: {msg}")

	