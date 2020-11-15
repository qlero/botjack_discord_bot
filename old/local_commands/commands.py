import cv2
from keras.models import load_model
from keras.preprocessing import image
import numpy as np
import random
from urllib.request import Request, urlopen

def main_help(functions, author):
	"""
	Prints the !help message to the chat.
	-----
	:param <functions>: <class 'dict'> ; dictionary of available botjack commands
	:param <author>: <class 'str'> ; author of the command
	"""
	msg = ""
	for index, key in enumerate(functions.keys()):
		msg += key + ", " if index + 1 < len(functions) else key
	else:
		msg = f"**Available Commands**\nHello {author}. I currently have {len(functions)} functions or commands." + \
		"```" + msg + "```\nFor help with a particular command, use ``!help`` followed by the command name."
	return msg

def specific_help(functions, func):
	"""
	Prints the specific ?help <command> message to the chat.
	-----
	:param <functions>: <class 'dict'> ; dictionary of available botjack commands
	:param <func>: <class 'str'> ; command requested by user
	"""
	msg = "Beep, boop! I'm not a smart pony!"
	if (func in functions.keys()) or ("!" + func in functions.keys()):
		msg = functions[func] if func in functions.keys() else functions["!" + func]
	return msg

def avatar(author):
	"""
	Cites the creator of botjack's avatar.
	-----
	:param <author>: <class 'str'> ; author of the command
	"""
	msg = f"Hello {author}.\nMy avatar was made by: ScarfyAce. Please check their reddit:\n" + \
	"https://www.reddit.com/user/ScarfyAce/"
	return msg

def roll(roll, author):
	"""
	Rolls dice as requested by a user.
	-----
	:param <roll>: <class 'str'> ; snippets of user message after !roll
	:param <author>: <class 'str'> ; author of the command
	"""
	msg = "*Urgh*!"
	if len(roll) < 3: return msg
	
	print(f"{author} requested a die throw.")
	
	split = roll.split("d")
	if len(split) == 2:
		if ((split[0].isdigit() and split[1].isdigit()) and
			(int(split[0]) != 0 and int(split[1]) != 0)):
			msg = f"{(random.randrange(0, int(split[1]))+1) * int(split[0])}"
	
	return msg

def run_model(path):
	"""
	Runs the ML-trained model.
	-----
	:param <path>: String ; path of model
	"""
	model = load_model(path)	
	model.compile(loss = "binary_crossentropy", optimizer = "adam", metrics = ["accuracy"])
	return model
	
def ml_check(attachments, model, embed):
	"""
	Checks whether the picture is safe or unsafe based on a ML-trained model
	-----
	:param <attachments>: <class 'discord.message.Message.attachments'> ; metadata of the user 
	message's atachment
	:param <model>: <HDF5 dataset>  ; trained ML model, see Model 1 here: https://github.com/LMquentinLR/MLpy
	:param <embed>: <boolean>  ; indicates if the attachment is a direct one or an embed
	"""
	
	def load_image(url):
		"""
		Formats an image to fit the ML-trained model
		-----
		:param <url>: String ; url of image to test
		"""
		req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
		url_response = urlopen(req).read()
		img_array = np.array(bytearray(url_response), dtype=np.uint8)
		img = cv2.imdecode(img_array, 0)
		img = cv2.resize(img, (256,256))
		img = np.reshape(img, [-1, 256, 256, 1])
		return img
		
	msg = "Beep, boop! I'm not a smart pony!"
	pic_ext = [".jpg", ".png", ".jpeg"]
	
	if embed:
		attachment = attachments
	else:
		attachment = attachments[0].url
	
	try:
		for ext in pic_ext:
			if attachment.endswith(ext):
				img = load_image(attachment)
				classes = model.predict_classes(img, verbose=0)
				print(classes, type(classes))
				msg = ""
				if classes[0] == 0:
					msg += "Adam-optimized model says 'safe picture!'\n" 
				else: 
					msg += "Adam-optimized model says 'LOOD!'\n"
	except Error as e:
		print(e)
	return msg