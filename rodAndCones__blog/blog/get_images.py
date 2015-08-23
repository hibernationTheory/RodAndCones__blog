#get the images from imgur using it's api, 
#you will need to be registered to have client id and key
#save images into your local, if exists check to see if they changed before saving.

import json
import os
import sys

from imgurpython import ImgurClient
import requests

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, os.pardir))
CONFIG_FILE_NAME = "config_private.json"
CONFIG_FILE_PATH = os.path.join(ROOT_DIR, CONFIG_FILE_NAME)
PAGES_DIR = os.path.join(CURRENT_DIR, 'pages')
IMAGES_DIR = os.path.join(PAGES_DIR, 'images')


def get_all_image_data(config_file_path = CONFIG_FILE_PATH):
	"""gets all the images for the given user from imgur"""
	"""assumes you have a imgur api access"""

	images_all_data = []

	with file(config_file_path, "r") as config_file:
		config_data = json.load(config_file)

	client_id = config_data["imgur"]["client_id"]
	client_secret = config_data["imgur"]["client_secret"]
	username = config_data["imgur"]["username"]

	client = ImgurClient(client_id, client_secret)

	images = client.get_account_images(username)
	for image in images:
		image_data = {
						"title":image.title, 
						"link":image.link, 
						"size":image.size
					}
		images_all_data.append(image_data)

	return images_all_data


def download_all_images(data, dir = IMAGES_DIR):

	for image_data in data:
		name = image_data["title"]
		link = image_data["link"]
		size = image_data["size"]
		file_path = os.path.join(IMAGES_DIR, name)

		if os.path.exists(file_path):
			current_size = os.path.getsize(file_path)
			if current_size == size:
				print("skipping file since file size in disk is same: %s" %name)
				continue
		download_from_url(link, file_path)
	return True

def download_from_url(url, file_path):
	r = requests.get(url, stream=True)
	with open(file_path, 'wb') as fd:
	    for chunk in r.iter_content(20):
	        fd.write(chunk)
	return True

def main():
	image_data = get_all_image_data()
	download_all_images(image_data)

if __name__ == '__main__':
	main()

	