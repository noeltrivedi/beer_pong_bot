#!/usr/bin/python

import os
import json

'''
Retrieves the user's GroupMe access token from /data/groupme_access_token.json and
returns it. Returns "-1" if credentials file cannot be found.
'''
def _get_access_token():
	credentials_path = os.path.join('..', 'data', 'groupme_access_token.json')
	if not os.path.exists(credentials_path):
		print("Error loading GroupMe access token from /data/groupme_access_token.json")
		return "-1"
	with open(credentials_path) as file:
		data = json.load(file)
		return data['access_token']

'''
Recursively converts dictionary keys to strings.  Returns converted data.
'''
def _convert_keys_to_string(dictionary):
    if not isinstance(dictionary, dict):
        return dictionary
    return dict((str(k), _convert_keys_to_string(v)) 
        for k, v in dictionary.items())
