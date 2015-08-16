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
PAGES_DIR = settings.BLOG_PAGES_PATH

def get_sorted_files_names_from_path(pages_dir):
	unsorted_file_names = os.listdir(pages_dir)
	unsorted_file_names_full_path = [os.path.join(pages_dir, file_path) for file_path in unsorted_file_names]
	file_names = sorted(unsorted_file_names_full_path, key=os.path.getctime)
	return file_names

def get_all_pages(pages_dir, category='all'):
	file_names = get_sorted_files_names_from_path(pages_dir)

	allowed_extensions = ['.md']
	content = []
	for path in file_names:
		name = os.path.split(path)[1]
		nameExtension = os.path.splitext(name)[1]
		if nameExtension not in allowed_extensions:
			continue
		file_path = os.path.join(pages_dir, name)
		content_data = generate_page_data(name, pages_dir)
		content.append(content_data)

	return content

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

def convert_filename_to_title(name):
	title = name.replace('_', ' ').title()
	basename = os.path.splitext(title)[0]
	return basename

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

def generate_page_data(name, pages_dir):
	"""get or generate all the data for the view"""
	print("generate_page_data")

	content_data = {}
	nameBase = os.path.splitext(name)[0]
	file_full_path = os.path.join(pages_dir, name)
	print(file_full_path)

	page_content = get_page_content_or_404(name, pages_dir)
	header_image_path = get_header_image_path(page_content)
	if header_image_path:
		content_data['header_image'] = header_image_path
		page_content = remove_header_image_line(page_content)
	content_data['name'] = nameBase
	content_data['category'] = determine_post_category(nameBase)
	content_data['content'] = page_content
	file_time = time.ctime(os.path.getctime(file_full_path))
	file_time_formatted = datetime.datetime.strptime(file_time,  "%a %b %d %H:%M:%S %Y")
	content_data['date'] = file_time_formatted
	content_data['title'] = extract_html_text_from_content(page_content, 'h1')
	content_data['subtitle'] = extract_html_text_from_content(page_content, 'h2')
	first_paragraph = extract_html_text_from_content(page_content, 'p')

	content_data['first_paragraph'] = shorten_text(first_paragraph, 30)
	content_data['short_content'] = construct_front_page_post_content(content_data['category'], 
										content_data['title'], 
										content_data['first_paragraph'])
	return content_data

def construct_front_page_post_content(content_type, title, first_paragraph):
	quote_types = ["quote", "passage"]
	if content_type not in quote_types:
		new_title = "<h1>" + title + "</h1>"
		new_paragraph = "<p>" + first_paragraph + "</p>"
		content = new_title + new_paragraph
	else:
		content = "<blockquote>" + first_paragraph + "</blockquote>"
	return content


def shorten_text(text, word_limit):
	"""given the text, limit it to amount of words that are below or equal to given word limit"""
	word_data = text.split(" ")
	if len(word_data) > word_limit:
		word_data = word_data[:word_limit]
		text = " ".join(word_data) + "..."
	return text

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

def get_page_content_or_404(name, pages_dir):
	try:
		file_path = os.path.join(pages_dir, name)
	except ValueError:
		raise Http404('Page Not Found')
	else:
		if not os.path.exists(file_path):
			raise Http404('Page Not Found')

	with open(file_path, 'r') as f:
		page_string = unicode(f.read(), 'utf-8')

	html = markdown.markdown(page_string)
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

def index(request, pagenum=1, category='all', pages_dir=PAGES_DIR):
	print(index)
	category_names = ['quote', 'passage', 'opinion', 'all']
	if category not in category_names:
		raise Http404('Page Not Found')

	url = reverse('blog-pages')
	print(url)
	if category != 'all':
		url = reverse('blog-categories', kwargs={'category':category})

	page_data = get_all_pages(pages_dir, category)
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

def post_page(request, title, pages_dir=PAGES_DIR):
	print("post_page")
	if title.endswith('/'):
		title = title[:-1]
	if title.startswith('/'):
		title = title[1:]
	file_title = '{}.md'.format(title)
	page_content = generate_page_data(file_title, pages_dir)
	data = {'data':page_content}
	return render_to_response('post_page.html', data)