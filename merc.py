import discord
from discord.ext import commands

from tools.useful_functions import log

class Merciless(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self._last_member = None
		self.id_list = []

	@commands.Cog.listener()
	async def on_message(self, message):
		if message.author == self.bot.user:
			return

		if not message.guild:
			if "nicknuke" in message.content:
				await self.nick_nuke(message)

		#DEPRECIATED#
		#role-request
		#if message.channel.id == 834565569180991488: 
		#	await self.rolecaller(message)
		
		#hll-admin-log
		if message.channel.id == 968889649428848650 and message.author.name == "Hook of War":
			await self.modify_log_webhook(message)

		#hll-admin-ping
		if message.channel.id == 968984419828375662 and message.author.name == "Hook of War":
			await self.modify_help_webhook(message)

	#-------------------------------------------------------------------------------------------------------- nicknuke
	async def nick_nuke(self, message):
		id = message.author.id
		if id in self.id_list:
			self.id_list.remove(id)
			await message.channel.send("I will stop preventing your nickname from being changed on servers we share.")
			log(f"UPD: {message.author.name} ({message.author.id}) removed from nicknuke list via DM.")
		else:
			self.id_list.append(id)
			await message.channel.send("I will prevent your nickname from being changed on servers we share.")
			log(f"UPD: {message.author.name} ({message.author.id}) added to nicknuke list via DM.")


	#-------------------------------------------------------------------------------------------------------- rolecaller
	'''DEPRECIATED!
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

		#role given: "V-rising"
		if "v-rising" in msg or "v rising" in msg or "vrising" in msg:
			if (await self.give_role(message, 978189792049242132)):
				await message.add_reaction("<:vrising:978287390030430208>")

		#role given: "Tarkov"
		if "tarkov" in msg:
			if (await self.give_role(message, 985266644928561182)):
				rolegiven = True

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
			if (await self.give_role(message, 983830851441799218)): # 983830851441799218
				await message.add_reaction("<:foxhole:985934949708341248>")

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
		return False
	'''
	#-------------------------------------------------------------------------------------------------------- modify_log_webhook
	async def modify_log_webhook(self, message):
		msg = message.content

		#Formats the server name and adds coloration via code blocks
		msg = msg.replace("[MERC] -US WEST L.A Discord.GG/m3rc", "```ini\n[US WEST]")
		msg = msg.replace("[Merc] US East D.C  Discord.gg/m3rc", "```css\n[US EAST]")
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

		#formats the incoming ping, removing uneccessary information
		msg = msg.replace("[MERC] -US WEST L.A Discord.GG/m3rc", "US WEST")
		msg = msg.replace("[Merc] US East D.C  Discord.gg/m3rc", "US EAST")
		msg = msg.replace("!adminhelp", "")
		msg = msg.replace("!ADMINHELP", "")
		msg = msg.replace("!admin", "")
		msg = msg.replace("!ADMIN", "")

		msg_with_mention = "<@&1098116700920090704> " + msg

		try:
			await message.channel.send(msg_with_mention)
		except:
			log(f"ERR: Failed to format webhook, aborting delete.")
		else:
			await message.delete()

		log(f"LOG: {msg}")

	@commands.Cog.listener()
	async def on_member_update(self, before, after):
		
		for id in self.id_list:
			if after.id == id:
				if after.nick:
					await after.edit(nick=None)

	#Open Mic Knight on Merc = 1114692562553413632
	#Member on Merc = 697529828282335272
	#Merc = 653042329938034739
	@commands.Cog.listener()
	async def on_member_join(self, member):
		if member.guild.id == 653042329938034739:
			role = discord.utils.get(member.guild.roles, id=1114692562553413632)
			if role and role not in member.roles:
				await member.add_roles(role)
				log(f"UPD: {member.name} joined {member.guild.name}, automatically assigned {role.name}")
			else:
				log(f"UPD: {member.name} joined {member.guild.name}, already assigned {role.name}")
			
			role = discord.utils.get(member.guild.roles, id=697529828282335272)
			if role and role not in member.roles:
				await member.add_roles(role)
				log(f"UPD: {member.name} joined {member.guild.name}, automatically assigned {role.name}")
			else:
				log(f"UPD: {member.name} joined {member.guild.name}, already assigned {role.name}")

	@commands.command(name="knighthood", hidden=True)
	async def open_mic_knighthood(self, ctx):
		if not ctx.message.author.guild_permissions.administrator:
			return
		
		await ctx.send("Beginning update. Warning: this may take some time...")
		num_updated = 0
		for guild in self.bot.guilds:
			if ctx.guild.id == 653042329938034739:
				role = discord.utils.get(guild.roles, id=1114692562553413632)
				for member in guild.members:
					if role and role not in member.roles:
						await member.add_roles(role)
						num_updated = num_updated + 1
						log(f"UPD: {member.name} given {role.name} in {guild.name}.")
		if num_updated:
			log(f"LOG: Finished updating {num_updated} members in {ctx.guild.name}")
			await ctx.send(f"Finished updating {num_updated} members.")
		else:
			log(f"LOG: Knighthood found no knaves...")
			await ctx.send("It appears everyone is a knight already.")

	async def give_role(self, member, id) -> bool:
		role = discord.utils.get(member.guild.roles, id=id)
		if role and role not in member.roles:
			await member.add_roles(role)
			log(f"UPD: {message.author} given {role}")
			return True
		return False	


	@commands.command(name="nicknuke", hidden=True)
	async def nickname_nuke(self, ctx, *args):
		id = ctx.author.id
		if id in self.id_list:
			self.id_list.remove(id)
			await ctx.send("Your nickname can be changed now", delete_after=3.0)
			log(f"UPD: {ctx.author.name} ({ctx.author.id}) removed from nicknuke list via command.")
		else:
			self.id_list.append(id)
			await ctx.send("Your nickname can no longer be changed", delete_after=3.0)
			log(f"UPD: {ctx.author.name} ({ctx.author.id}) added to nicknuke list via command.")
		
		await ctx.message.delete()

	@commands.command(name="clearnicknuke", hidden=True)
	@commands.has_permissions(administrator=True)
	async def clear_nickname_nuke(self, ctx):
		self.id_list = []
		await ctx.send("nicknuke list cleared.", delete_after=3.0)
		log(f"UPD: Nicknuke list cleared by administrator {ctx.author.name} ({ctx.author.id}).")
		await ctx.message.delete()