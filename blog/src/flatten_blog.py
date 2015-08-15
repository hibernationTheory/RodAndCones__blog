"""
import json
import markdown
import os
import time
from HTMLParser import HTMLParser

from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.conf import settings

from bs4 import BeautifulSoup
"""
import os
import sys

CURRENT_DIR = os.getcwdu()
PARENT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, os.pardir))

if PARENT_DIR not in sys.path:
	sys.path.insert(0, PARENT_DIR)

from django.conf import settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'rodAndCones.settings'

from django.template.loader import render_to_string as rts
from django.core.urlresolvers import reverse
from django.test.client import Client

import views

PAGES_DIR = views.PAGES_DIR
PAGE_DATA_FILE = views.PAGE_DATA_FILE
BLOG_PAGES_PATH = settings.BLOG_PAGES_PATH
BLOG_TEMPLATE_PATH = settings.BLOG_TEMPLATE_PATH
POST_PAGE_TEMPLATE = os.path.join(BLOG_TEMPLATE_PATH, "post_page.html")
print(POST_PAGE_TEMPLATE)

def get_pages():
	for name in os.listdir(BLOG_PAGES_PATH):
		if os.path.splitext(name)[1] == '.md':
			yield os.path.splitext(name)[0]

all_pages_data = views.get_all_pages(PAGES_DIR, PAGE_DATA_FILE)

for page in get_pages():
	for datum in all_pages_data:
		if datum["name"] == page:
			page_data = {"data":datum}
			rendered = rts(POST_PAGE_TEMPLATE, page_data)
			print(rendered)