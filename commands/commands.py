import cv2
from keras.models import load_model
from keras.preprocessing import image
import numpy as np
import os
import random
from urllib.request import Request, urlopen

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

def run_model():
	"""
	Runs the ML-trained model.
	No arguments
	"""
	dirname, filename = os.path.split(os.path.abspath(__file__))
	model = load_model(dirname + "\\model.h5")
	model.compile(loss = "binary_crossentropy",
				optimizer = "rmsprop",
				metrics = ["accuracy"])
	return model
	
def ml_check(attachments, model):
	"""
	Checks whether the picture is safe or unsafe based on a ML-trained model
	:param <attachments>: TBD ; TBD
	:param <model>: TBD ; TBD
	"""
	
	def load_image(url):
		"""
		Formats an image to fit the ML-trained model
		:param <url>: String ; url of image to test
		"""
		req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
		url_response = urlopen(req).read()
		img_array = np.array(bytearray(url_response), dtype=np.uint8)
		img = cv2.imdecode(img_array, 0)
		img = cv2.resize(img, (224,224))
		img = np.reshape(img, [-1, 224, 224, 1])
		return img
		
	msg = "Beep, boop! I'm not a smart pony!"
	pic_ext = [".jpg", ".png", ".jpeg"]
	
	attachment = attachments[0].url
	
	for ext in pic_ext:
		if attachment.endswith(ext):
			img = load_image(attachment)
			classes = model.predict_classes(img, verbose=0)
			#classes = model.predict_proba(img, verbose=1)
			print(classes)
			print(type(classes))
			if classes[0] == 0:
				msg = "This picture is safe for work."
			else:
				msg = "This picture is lood!"
	
	return msg