#get the gist data for a user
#save the gists into your local, check to see if they changed before saving.

import datetime
import os
import json

#3rd party
import requests
import markdown

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
PAGES_DIR = os.path.join(CURRENT_DIR, 'pages')

GITHUB_USER_NAME = "hibernationTheory"
GITHUB_GIST_URL = "https://api.github.com/gists/"
GITHUB_USER_GIST_URL = "https://api.github.com/users/" + GITHUB_USER_NAME + "/gists"

def get_gist_data_from_github(username=GITHUB_USER_NAME):
	"""gets all the gists for the given user from the github gists"""
	website = "https://api.github.com/users/"
	user_gists = website + username + "/gists"
	response = requests.get(user_gists)
	if not response.ok:
		return None
	data = [i for i in response.json()]
	return data

def get_content_data_for_all_gists(gist_data_all):
	"""gets the content from all the files"""
	if not gist_data_all:
		return None
	content_data = []

	for gist in gist_data_all:
		gist_id = gist['id']
		files_dict = gist['files']
		md_content = None

		for file_item in files_dict.iteritems():
			file_name = file_item[0]
			file_item_data = file_item[1]

			language = file_item_data['language']
			if language == 'Markdown' and not file_name.startswith('__'):
				markdown_data = file_item_data
				download_gist_markdown(file_name, file_item_data)
				continue

def download_gist_markdown(name, data, dir = PAGES_DIR):
	file_path = os.path.join(PAGES_DIR, name)
	if os.path.exists(file_path):
		current_size = os.path.getsize(file_path)
		if current_size == data["size"]:
			print("skipping file since file size in disk is same: %s" %name)
			return
	download_from_url(data["raw_url"], file_path)
	return True

def download_from_url(url, file_path):
	r = requests.get(url, stream=True)
	with open(file_path, 'wb') as fd:
	    for chunk in r.iter_content(20):
	        fd.write(chunk)
	return True

def main():
	gist_data_all = get_gist_data_from_github()
	get_content_data_for_all_gists(gist_data_all)

main()
	