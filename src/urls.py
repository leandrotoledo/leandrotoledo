from django.conf.urls.defaults import patterns, include, url
from django.views.generic import ListView, DetailView, RedirectView
from django.views.generic.dates import MonthArchiveView
from django.contrib import admin
from django.contrib.sitemaps import FlatPageSitemap, GenericSitemap

from core.feeds import PostsFeed
from core.models import Category, Post
from core.sitemaps import PostsSitemap

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/',     include(admin.site.urls)),
    url(r'^comments/',  include('django.contrib.comments.urls')),

    url(r'^$',
        ListView.as_view(queryset=Post.objects.filter(is_draft=False), paginate_by=4),
        name='index'),
        
	(r'^feed/$',
		PostsFeed()),

    (r'^posts/$',
        RedirectView.as_view(url='/')),

    (r'^categories/$',
        RedirectView.as_view(url='/')),

    # TOFIX
    (r'^robots\.txt$',
        RedirectView.as_view(url='/static/robots.txt')),

    url(r'^posts/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/$',
        DetailView.as_view(model=Post),
        name='post'),

    url(r'^posts/(?P<year>\d{4})/(?P<month>\d{1,2})/$',
        MonthArchiveView.as_view(model=Post, date_field='published_date', month_format='%m'),
        name='archive_month'),

    url(r'^categories/(?P<category>[-\w]+)/$',
        ListView.as_view(model=Category),
        name='category'),
)

sitemaps = {
    'flatpages': FlatPageSitemap,
    'posts': PostsSitemap()
}

urlpatterns += patterns('django.contrib.sitemaps.views',
    (r'^sitemap\.xml$', 'sitemap', {
        'sitemaps': sitemaps,
        'template_name': 'sitemap.xml'
    }),
)
