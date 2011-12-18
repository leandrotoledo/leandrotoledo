from django.conf.urls.defaults import patterns, include, url
from django.views.generic import ListView

from core.models import Post

urlpatterns = patterns('',
	url(r'^$', ListView.as_view(model=Post, template_name='index.html'), name='index'),
)
