import urllib.request
from urllib.parse import quote
import json
import random
import traceback
import numpy as np

TOKEN = 'https://api.telegram.org/bot866724568:AAFnq-pnAOZQFEsRfpjZuzmcdgnuH5wl7Vw/'

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

while True:
	r = callMethod('getUpdates',offset=current_update_id) # Gets latest update

	# Scan to see if the latest update is new or already received
	if r['result'][-1]['update_id']!=current_update_id:
		current_result = r['result'][-1]
		current_update_id = current_result['update_id']
		try:
			current_message_id = current_result['message']['message_id']
			current_chat = current_result['message']['chat']

			# print(current_result)
			
			# Separate response to private messages
			if current_chat['type']=='private':
				callMethod('sendMessage', chat_id = current_chat['id'],
					text = 'Hi, I am a bot based on the New Age Bullshit Generator. '
							'To use me, add me to a group and send a message tagged to me.')

			elif current_chat['type']=='group' or current_chat['type']=='supergroup':
				# Trying to get the bot to recognise its mention
				if 'entities' in current_result['message']:
					# print(current_result['message']['entities'])
					for ent in current_result['message']['entities']:
						if 'type' in ent:
							if ent['type']=='mention':
								callMethod('sendMessage', chat_id = current_chat['id'],
								text = 'Selfishness is the antithesis of coherence.',
								reply_to_message_id = current_message_id)

		except Exception as e:
			print(traceback.format_exc())
			print(current_result)