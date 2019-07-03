#!/usr/bin/python

import requests
import os
import json
from Util import _get_access_token, _convert_keys_to_string

DEBUG = True

'''
Sends a POST request to GroupMe servers to start a new GroupMe chat, and 
returns the group_id.
'''
def create_group_POST():
	# Allow for users to modify the create_request.json to easily customize their Beer Pong group creation.
	request_path = os.path.join('.', 'requests', 'create_request.json')
	if not os.path.exists(request_path):
		# Load default values.
		payload = '{ "name": "Beer Pong", "description": "Let ball meet beer.", "share": true, "image_url": "https://i.groupme.com/355x265.jpeg.45df9565ba15494caaffbe7fa899fe59" }'
	else:
		payload = open(request_path)

	# Send request.
	url = 'https://api.groupme.com/v3/groups?token=' + _get_access_token()
	headers = {'Content-Type': 'application/json', 'Accept-Charset': 'UTF-8'}
	response = requests.post(url, data=payload, headers=headers)

	# Status 201 is success.
	if response.status_code != 201:
		print("Error POST requesting GroupMe servers when creating new group.  Status code: " + str(response.status_code))
		exit(1)
	data = _convert_keys_to_string(response.json())

	# Return group_id to pass into create_bot_POST().
	return int(data['response']['group_id'])

'''
Sends a POST request to GroupMe servers to create a new bot.
'''
def create_bot_POST(group_id, port, callback_url=None):
	request_path = os.path.join('.', 'requests', 'bot_request.json')
	if not os.path.exists(request_path) or callback_url is not None or DEBUG:
		# Load default values.
		payload = '{ "bot": { "name": "Chomps", "group_id": "' + str(group_id) + '", "callback_url": "' + str(callback_url) + '", "avatar_url": "https://i.groupme.com/2533x2533.jpeg.f3668bffbc03412da7718d2d34426e05" } }'
	'''
	else:
		file = open(request_path)
		payload = _convert_keys_to_string(json.load(file))
		payload['bot']['group_id'] = str(group_id)
		payload['bot']['callback_url'] += str(port)
		for item in payload['bot']:
			payload['bot'][item] = str(payload['bot'][item])
	'''
	# Send request.
	url = 'https://api.groupme.com/v3/bots?token=' + _get_access_token()
	headers = {'Content-Type': 'application/json', 'Accept-Charset': 'UTF-8'}
	response = requests.post(url, data=payload, headers=headers)

	# Status 201 is success.
	if response.status_code != 201:
		print("Error POST requesting GroupMe servers when initializing your Chomps.  Status code: " + str(response.status_code))
		exit(1)
	converted_response = _convert_keys_to_string(response.json())

	# Have Chomps send a welcome message to the group.
	bot_id = str(converted_response['response']['bot']['bot_id'])
	request = '{ "bot_id": "' + bot_id + '", "text": "Hello, my name is Chomps.  Let ball meet beer.  Type !help to see a list of commands and instructions on how to use Chomps." }'
	url = "https://api.groupme.com/v3/bots/post"
	response = requests.post(url, data=request, headers=headers)

port = 4999
create_bot_POST(create_group_POST(), port, "http://noeltrivedi.com:4999")