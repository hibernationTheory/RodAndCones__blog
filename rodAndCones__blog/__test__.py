import requests, json
import markdown
import datetime

GITHUB_USER_NAME = "hibernationTheory"
GITHUB_GIST_URL = "https://api.github.com/gists/"
GITHUB_USER_GIST_URL = "https://api.github.com/users/" + GITHUB_USER_NAME + "/gists"

#gist_url = GITHUB_GIST_URL + item['id']

x = datetime.datetime.strptime("2013-05-02T16:46:04Z", "%Y-%m-%dT%H:%M:%SZ")
print(x)

CATEGORY_DICT = {
	"_q_":"quote",
	"_r_":"review",
	"_p_":"passage"
}

def get_all_the_gists(username):
	"""gets all the gists for the given user"""
	website = "https://api.github.com/users/"
	user_gists = website + username + "/gists"
	response = requests.get(user_gists)
	if not response.ok:
		return None
	data = [ i for i in response.json() ]
	return data

def sort_the_gists():
	"""sorts the gists according to their creation time"""
	pass

def filter_gists_by_category(gist_data, category="all"):
	"""helper function to filter gists based on their category"""
	if not gist_data:
		return None
	files_dict = gist_data["files"]
	for file_item in files_dict.iteritems():
		file_name = file_item[0]
		file_item_data = file_item[1]
		language = file_item_data["language"]

		if language == "Markdown":
			md_content = file_item_data["content"]

def determine_post_category(name):
	category = 'opinion'
	if name.startswith('_'):
		if name.startswith('_p_'):
			category = 'passage'
		elif name.startswith('_q_'):
			category = 'quote'
		else:
			category = 'opinion'
	return category

def get_content_for_all_gists(gist_data, category="all"):
	"""gets the content from all the files"""
	if not gist_data:
		return None
	content_data = []
	for gist in gist_data:
		gist_id = gist['id']
		files_dict = gist['files']
		md_content = None
		for file_item in files_dict.iteritems():
			file_name = file_item[0]
			file_item_data = file_item[1]

			language = file_item_data['language']
			if language == 'Markdown':# and not file_name.startswith('__'):
				append = False
				if category != "all":
					current_category = determine_post_category(file_name)
					if current_category == category:
						append = True
				else:
					append = True

				if append:
					gist_data = get_single_gist_data(gist_id)
					print(gist_data)
					return
					md_content = gist_data['content']
					content_data.append(md_content)

	return content_data

def get_single_gist_data(given_id):
	'''gets the data for the gist with the given id'''
	url = "https://api.github.com/gists/" + given_id
	response = requests.get(url)
	if not response.ok:
		return None
	return response.json()



all_gists = get_all_the_gists("hibernationTheory")
all_content = get_content_for_all_gists(all_gists)
print(all_content)


"""
"""
import datetime
import json
import os
import sys
import time
from HTMLParser import HTMLParser

CURRENT_DIR = os.getcwdu()
PARENT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, os.pardir))

if PARENT_DIR not in sys.path:
	sys.path.insert(0, PARENT_DIR)

from django.conf import settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'rodAndCones.settings'

from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core import serializers
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from django.template import RequestContext
from django.shortcuts import render_to_response

# 3rd party Python modules
from bs4 import BeautifulSoup
import markdown
import requests

# globals
GITHUB_USER_NAME = "hibernationTheory"
GITHUB_GIST_URL = "https://api.github.com/users/" + GITHUB_USER_NAME + "/gists"

def get_all_page_data(username=GITHUB_USER_NAME, category='all'):
	gist_data = get_gist_data_from_github(username)
	page_data = get_content_data_for_all_gists(gist_data, category)
	return page_data


def get_gist_data_from_github(username=GITHUB_USER_NAME):
	"""gets all the gists for the given user from the github gists"""
	website = "https://api.github.com/users/"
	user_gists = website + username + "/gists"
	response = requests.get(user_gists)
	if not response.ok:
		return None
	data = [ i for i in response.json() ]
	return data

def get_content_data_for_all_gists(gist_data_all, category="all"):
	"""gets the content from all the files"""
	if not gist_data_all:
		return None
	content_data = []

	for gist in gist_data_all:
		gist_id = gist['id']
		single_gist_data = get_single_gist_data(gist_id)
		files_dict = single_gist_data['files']
		md_content = None

		for file_item in files_dict.iteritems():
			file_name = file_item[0]
			file_item_data = file_item[1]

			language = file_item_data['language']
			if language == 'Markdown':# and not file_name.startswith('__'):
				append = False
				if category != "all":
					current_category = determine_post_category(file_name)
					if current_category == category:
						append = True
				else:
					append = True

				if append:
					markdown_data = file_item_data
					data = generate_page_data(markdown_data, single_gist_data)
					content_data.append(data)

	return content_data

def generate_page_data(markdown_data, single_gist_data):
	"""get or generate data from the gist data for rendering purposes"""
	print("generate_page_data")

	content_data = {}
	nameBase = os.path.splitext(markdown_data["filename"])[0]

	page_content = get_page_content(markdown_data)
	header_image_path = get_header_image_path(page_content)
	if header_image_path:
		content_data['header_image'] = header_image_path
		page_content = remove_header_image_line(page_content)
	content_data['name'] = nameBase
	content_data['category'] = determine_post_category(nameBase)
	content_data['content'] = page_content
	file_time = datetime.datetime.strptime(single_gist_data["created_at"], "%Y-%m-%dT%H:%M:%SZ")
	file_time_formatted = file_time.strftime("%a %b %d %H:%M:%S %Y")
	content_data['date'] = file_time_formatted
	content_data['title'] = extract_html_text_from_content(page_content, 'h1')
	content_data['subtitle'] = extract_html_text_from_content(page_content, 'h2')
	first_paragraph = extract_html_text_from_content(page_content, 'p')

	content_data['first_paragraph'] = shorten_text(first_paragraph, 30)
	content_data['short_content'] = construct_front_page_post_content(content_data['category'], 
										content_data['title'], 
										content_data['first_paragraph'])
	return content_data

def get_single_gist_data(given_id):
	'''gets the data for the gist with the given id'''
	url = "https://api.github.com/gists/" + given_id
	response = requests.get(url)
	if not response.ok:
		return None
	return response.json()


def filter_pages_by_category(page_data, category='all'):
	if category == 'all':
		return page_data
	content = []
	for content_data in page_data:
		if content_data['category'] != category:
			continue
		else:
			content.append(content_data)

	return content

def get_all_categories(pages_data):
	categories = {}

	for datum in pages_data:
		category_name = datum['category']
		if not categories.get(category_name, None):
			categories[category_name] = []
		categories[category_name].append({'name':datum['name'], 'title':datum['title']})

	return categories



def determine_post_category(name):
	category = 'opinion'
	if name.startswith('_'):
		if name.startswith('_p_'):
			category = 'passage'
		elif name.startswith('_q_'):
			category = 'quote'
		else:
			category = 'opinion'
	return category

def construct_front_page_post_content(content_type, title, first_paragraph):
	quote_types = ["quote", "passage"]
	if content_type not in quote_types:
		new_title = "<h1>" + title + "</h1>"
		new_paragraph = "<p>" + first_paragraph + "</p>"
		content = new_title + new_paragraph
	else:
		content = "<blockquote>" + first_paragraph + "</blockquote>"
	return content


def extract_html_text_from_content(content, element):
	soup = BeautifulSoup(content)
	soup_el = soup.find_all(element)
	if len(soup_el) == 0:
		print('given element doesn\'t exist in the file!')
		return ''
	else:
		soup_el = soup_el[0]

	text = ''
	if len(soup_el.contents) == 0:
		print('no content for the given element')
		return text
	else:
		text = soup_el.contents[0]

	return text

def get_page_content(markdown_data):
	html = markdown.markdown(markdown_data["content"])
	html = fix_html_img_tags_static_path(html)
	return html

def get_header_image(html):
	firstLine = html.splitlines()[0]
	if firstLine.find("<img") != -1:
		return firstLine
	else:
		return None

def get_header_image_path(html):
	"""
	it is assumed that if the first line of the content is an image file
	than it is intended to be a header image, 
	that image is treated differently in the layout
	so the src for it is fetched here
	"""
	firstLine = get_header_image(html)
	if not firstLine:
		return None
	target_str = 'src="'
	target_end_str = '" /></p>'
	len_target_str = len(target_str)

	pos = firstLine.find(target_str)
	end_pos = firstLine.find(target_end_str)
	url = firstLine[pos+len_target_str:end_pos]
	return url

def remove_header_image_line(html):
	"""
	it is assumed that if the first line of the content is an image file
	than it is intended to be a header image, 
	if that image exists, removes it from the content
	"""
	firstLine = get_header_image(html)
	if not firstLine:
		return None
	new_html = ''
	counter = 0
	for line in html.splitlines():
		if counter > 0:
			new_html += line
		counter += 1
	return new_html

def fix_html_img_tags_static_path(html):
	new_html = ''
	target_str = 'src="'
	len_target_str = len(target_str)

	if html.find('<img') != -1:
		for line in html.splitlines():
			if line.find('<img') != -1:
				pos = line.find(target_str)
				line = line[:pos+len_target_str] + static('') + line[pos+len_target_str:]
			new_html += line + '\n'
		return new_html
	else:
		return html

def index(request, pagenum=1, category='all'):
	category_names = ['quote', 'passage', 'opinion', 'all']
	if category not in category_names:
		raise Http404('Page Not Found')

	url = reverse('blog-pages')
	print(url)
	if category != 'all':
		url = reverse('blog-categories', kwargs={'category':category})

	page_data = get_all_page_data(username = GITHUB_USER_NAME, category=category)
	filtered_page_data = filter_pages_by_category(page_data, category)
	categories = get_all_categories(page_data)

	paginated_page_data = Paginator(filtered_page_data, 3)
	try:
		page = paginated_page_data.page(pagenum)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		page = paginated_page_data.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		raise Http404('Page Not Found')

	content = {'page_data':page, 'categories':categories, 'url':url}
	return render_to_response('index.html', content)

def post_page(request, title, pages_dir):
	print("post_page")
	if title.endswith('/'):
		title = title[:-1]
	if title.startswith('/'):
		title = title[1:]
	file_title = '{}.md'.format(title)
	page_content = generate_page_data(file_title, pages_dir)
	data = {'data':page_content}
	return render_to_response('post_page.html', data)

# UTILITY FUNCTIONS

def convert_filename_to_title(name):
	title = name.replace('_', ' ').title()
	basename = os.path.splitext(title)[0]
	return basename

def shorten_text(text, word_limit):
	"""given the text, limit it to amount of words that are below or equal to given word limit"""
	word_data = text.split(" ")
	if len(word_data) > word_limit:
		word_data = word_data[:word_limit]
		text = " ".join(word_data) + "..."
	return text
