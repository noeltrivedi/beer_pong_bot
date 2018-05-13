#!/usr/bin/python

import requests
import os
import json


def _get_access_token():
	credentials_path = os.path.join('.', 'data', 'groupme_access_token.json')
	if not os.path.exists(credentials_path):
		print("Error loading GroupMe access token from /data/groupme_access_token.json")
	else:
		with open(credentials_path) as file:
			data = json.load(file)
			return data['access_token']

def _create_group_POST():
	request_path = os.path.join('.', 'requests', 'create_request.json')
	if not os.path.exists(request_path):
		print("Error loading GroupMe access token from /data/groupme_access_token.json")
	payload = open(request_path)
	url = 'https://api.groupme.com/v3/groups?token=' + _get_access_token()
	print url
	headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
	response = requests.post(url, data=payload, headers=headers)

	print response



_create_group_POST()