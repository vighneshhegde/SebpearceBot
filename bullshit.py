import urllib.request
from urllib.parse import quote
import json
import random
import traceback
# import numpy as np
from svo import findSVOs
from spacy.lang.en import English

with open("TOKEN.txt", "r") as f:
    TOKEN = f.readline()[:-1]

sentences = []
with open("bullshit.txt", "r") as f:
    sentences = f.read().split('\n')

insults = []
with open("insults.txt", "r") as f:
    insults = f.read().split('\n')

def your_mom(current_message):
	# current_message['from']['first_name'] + ', ' + random.choice(insults)
	parser = English()

	try:
		text = current_message['text']
		parse = parser(text)
		print(text, parse, findSVOs(parse))


	except Exception:
		print(traceback.format_exc())
		print(current_message)


	joke = 'That\'s what your mom said last night'
	return joke

def callMethod(name, **kwargs):
	arg_string = ''
	count = 0
	for arg_name, arg_val in kwargs.items():
		if count == 0: 	arg_string = '?'
		else:			arg_string += '&'
		arg_string += arg_name + '=' + quote(str(arg_val).encode("utf-8"))
		count += 1

	r = urllib.request.urlopen(TOKEN + name + arg_string)

	return json.loads(r.read().decode('utf-8'))

current_update_id = 0

# print(sentences[10])

while True:
	r = callMethod('getUpdates', offset=current_update_id) # Gets latest update

	# Scan to see if the latest update is new or already received
	if r['result'][-1]['update_id']!=current_update_id:
		current_result = r['result'][-1]
		current_update_id = current_result['update_id']
		try:
			if 'message' in current_result:
				current_message = current_result['message']
			elif 'edited_message' in current_result:
				current_message = current_result['edited_message']
			current_message_id = current_message['message_id']
			current_chat = current_message['chat']

			print(current_result)
			# print(current_message['from']['first_name']+', '+random.choice(sentences))
			
			# Separate response to private messages
			if current_chat['type']=='private':
				callMethod('sendMessage', chat_id = current_chat['id'],
					text = 'Hi, I am a bot based on the New Age Bullshit Generator. '
							'To use me, add me to a group and send a message tagged to me.')

			elif current_chat['type']=='group' or current_chat['type']=='supergroup':
				# Trying to get the bot to recognise its mention
				if 'entities' in current_message:
					for ent in current_message['entities']:
						if 'type' in ent:
							if ent['type']=='mention' and '@sebpearcebot' in current_message['text']:
								# if 'user' in ent:
								# 	send message to that user
								callMethod('sendMessage', chat_id = current_chat['id'],
								text = current_message['from']['first_name']+', '+random.choice(sentences).lower(),
								reply_to_message_id = current_message_id)
				elif 'reply_to_message' in current_result['message'] and\
					current_result['message']['reply_to_message']['from']['id']==866724568:
						callMethod('sendMessage', chat_id = current_chat['id'],
								text = current_message['from']['first_name']+', '+random.choice(insults),
								reply_to_message_id = current_message_id)

				elif current_message['from']['id']==133119361:
					if random.random()<0.5:
						callMethod('sendMessage', chat_id=current_chat['id'],
							text=your_mom(current_message),
							reply_to_message_id=current_message_id)

		except Exception as e:
			print(traceback.format_exc())
			print(current_result)