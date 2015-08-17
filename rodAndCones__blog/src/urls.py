from django.conf.urls import patterns, include, url
from . import views

urlpatterns = patterns('',
	url(r"^categories/(?P<category>\w+)/(?P<pagenum>[0-9]+)/$", views.index, name="blog-categories-page"),
	url(r"^categories/(?P<category>\w+)/$", views.index, name="blog-categories"),
	url(r"^pages/(?P<pagenum>[0-9]+)/$", views.index, name="blog-pages-page"),
	url(r"^pages/$", views.index, name="blog-pages"),
	url(r"^(?P<title>[\w./-]+/$)", views.post_page, name="blog-post"),
	url(r"^$", views.index, name="blog-index")
)
