import random

def main_help(message, functions):
	"""
	Prints the !help message to the chat.
	:param <message>: <class 'discord.message.Message'> ; user message triggering a bot event
	:param <functions>: <class 'dict'> ; dictionary of available commands for botjack
	"""
	msg = ""
	for index, key in enumerate(functions.keys()):
		msg += key + ", " if index + 1 < len(functions) else key
	else:
		msg = f"**Available Commands**\nHello {message.author.mention}. I currently have {len(functions)} commands." + \
		"```" + msg + "```\nFor help with a particular command, use ``?help`` followed by the command name."
	return msg

def specific_help(message, functions):
	"""
	Prints the specific ?help <command> message to the chat.
	:param <message>: <class 'discord.message.Message'> ; user message triggering a bot event
	:param <functions>: <class 'dict'> ; dictionary of available commands for botjack	
	"""
	msg = "Beep, boop! I'm not a smart pony!"
	split_msg = str(message.content).split(" ")
	if (split_msg[1] in functions.keys()) or ("!" + split_msg[1] in functions.keys()):
		msg = functions[split_msg[1]] if split_msg[1] in functions.keys() else functions["!" + split_msg[1]]
	return msg

def avatar(message):
	"""
	Cites the creator of botjack's avatar.
	:param <message>: <class 'discord.message.Message'> ; user message triggering a bot event
	"""
	msg = f"Hello {message.author.mention}.\nMy avatar was made by: ScarfyAce. Please check their reddit:\n" + \
	"https://www.reddit.com/user/ScarfyAce/"
	return msg

def roll(message):
	"""
	Rolls dice requested by a user.
	:param <message>: <class 'discord.message.Message'> ; user message triggering a bot event
	"""
	msg = "Beep, boop! I'm not a smart pony!"
	if len(message.content) < 9 or "\n" in message.content: return msg
	
	split_msg = str(message.content).split(" ")
	print(f"{message.author.mention} requested a die throw.")
	
	for bit in split_msg[1:]: 
		if len(bit.strip()) < 3:
			if msg.startswith("Beep"): msg = f"Your results, {message.author.mention}!\n**<!>**: <nope>, "
			else: msg += "**<!>**: <nope>"
			continue
		
		if msg.startswith("Beep"): msg = f"Your results, {message.author.mention}!\n**" + bit.strip() + "**: "
		else: msg += "**" + bit.strip() + "**: "
		split = bit.strip().split("d")
		if len(split) == 2:
			if split[0].isdigit() and split[1].isdigit():
				if int(split[0]) != 0 and int(split[1]) != 0:
					msg += f"{(random.randrange(0, int(split[1]))+1) * int(split[0])}, "
		if msg[-2:] == ": ": msg += "<nope>, "
	return msg[:-2]