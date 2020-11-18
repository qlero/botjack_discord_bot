import numpy as np
import tensorflow as tf   
from tensorflow import keras
from tensorflow.keras import layers
from keras.layers import Dense, Conv2D, BatchNormalization, Activation, ZeroPadding2D
from keras.layers import AveragePooling2D, MaxPooling2D, Flatten, Add
from keras.models import Model
import cv2
import random
from urllib.request import Request, urlopen

def main_help(functions, author):
	"""
	Prints the !info message to the chat.
	-----
	:param <functions>: <class 'dict'> ; dictionary of available botjack commands
	:param <author>: <class 'str'> ; author of the command
	"""
	msg = ""
	for index, key in enumerate(functions.keys()):
		msg += key + ", " if index + 1 < len(functions) else key
	else:
		msg = f"**Available Commands**\nHello {author}. I currently have {len(functions)} functions or commands." + \
		"```" + msg + "```\nFor help with a particular command, use ``!info`` followed by the command name."
	return msg

def specific_help(functions, func):
	"""
	Prints the specific !info <command> message to the chat.
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
                    rnd = random.randint(1, (int(split[1])+1)*int(split[0]))
                    msg=f"{rnd}"
	
	return msg

def make_model(input_shape, num_classes):
	"""
	Creates a model based on a RNN architecture.
	-----
	:param <input_shape>: <class 'tuple'> ; image size in pixels
	:param <num_classes>: <class 'int'> ; batch size
	"""
	inputs = keras.Input(shape=input_shape)
	
	# Entry block
	x = layers.experimental.preprocessing.Rescaling(1.0 / 255)(inputs)
	x = Conv2D(32, kernel_size=(3, 3), strides=2, padding="same")(x)
	x = BatchNormalization()(x)
	x = Activation("relu")(x)

	x = Conv2D(64, kernel_size=(3, 3), padding="same")(x)
	x = BatchNormalization()(x)
	x = Activation("relu")(x)

	previous_block_activation = x  # Set aside residual

	for size in [32, 64, 128, 256]:
		
		x = layers.SeparableConv2D(size, kernel_size=(3, 3), padding="same")(x)
		x = BatchNormalization()(x)
		x = Activation("relu")(x)
		
		x = layers.SeparableConv2D(size, kernel_size=(3, 3), padding="same")(x)
		x = BatchNormalization()(x)
		x = Activation("relu")(x)
		
		x = MaxPooling2D((3, 3), strides=2, padding="same")(x)

		# Project residual
		residual = Conv2D(size, kernel_size=(1, 1), strides=2, padding="same")(
			previous_block_activation
		)
		x = layers.add([x, residual])  # Add back residual
		previous_block_activation = x  # Set aside next residual

	x = layers.SeparableConv2D(128, kernel_size=(3, 3), padding="same")(x)
	x = BatchNormalization()(x)
	x = Activation("relu")(x)

	x = layers.GlobalAveragePooling2D()(x)
	if num_classes == 2:
		activation = "sigmoid"
		units = 1
	else:
		activation = "softmax"
		units = num_classes

	x = layers.Dropout(0.5)(x)
	outputs = layers.Dense(units, activation=activation)(x)
	return keras.Model(inputs, outputs)

def run_model(path):
	"""
	Runs the ML-trained model.
	-----
	:param <path>: String ; path of model
	"""
	image_size = (256, 256)
	model = make_model(input_shape=image_size + (3,), num_classes=2)
	model.compile(optimizer=keras.optimizers.Adam(1e-3), loss="binary_crossentropy", metrics=["accuracy"])
	model.load_weights(path)
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
		r = urlopen(req)
		image = np.asarray(bytearray(r.read()), dtype="uint8")
		image = cv2.imdecode(image, cv2.IMREAD_COLOR)
		image = cv2.resize(image, (256,256))
		img_array = keras.preprocessing.image.img_to_array(image)
		img_array = tf.expand_dims(img_array, 0) 
		return img_array
	#	req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
	#	url_response = urlopen(req).read()
	#	img_array = np.array(bytearray(url_response), dtype=np.uint8)
	#	img = cv2.imdecode(img_array, 0)
	#	img = cv2.resize(img, (256,256))
	#	img = np.reshape(img, [-1, 256, 256, 1])
	#	return img
		
	msg = "Beep, boop! I'm not a smart pony!"
	pic_ext = [".jpg", ".png", ".jpeg", ".PNG", ".JPEG", ".JPG"]
	
	if embed:
		attachment = attachments
	else:
		attachment = attachments[0].url
	
	#try:
	for ext in pic_ext:
		if attachment.endswith(ext):
			img = load_image(attachment)
			prediction = model.predict(img)
			msg = ""
			score = prediction[0]
			if score[0] > 0.6:
				msg += "This is SFW\n" 
			else: 
				msg += f"I am {round(100*(1-score[0]),2)}% certain this is NSFW\n"
	#except Error as e:
	#	print(e)
	return msg
