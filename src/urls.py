from django.conf.urls.defaults import patterns, include, url
from django.views.generic import RedirectView
from django.contrib import admin
from django.contrib.sitemaps import FlatPageSitemap
from django.conf import settings

from core.views import *
from core.feeds import PostsFeed
from core.models import Category, Post
from core.sitemaps import CategoriesSitemap, PostsSitemap

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^comments/', include('django.contrib.comments.urls')),

    url(r'^$',
        PostsListView.as_view(),
        name='index'),

    url(r'^feed/$',
        PostsFeed(),
        name='feeds'),

    url(r'^search/$',
        PostSearch.as_view(),
        name='search'),

    url(r'^pages/contact/$',
        Contact.as_view(),
        name='contact'),

    url(r'^pages/contact/thanks/$',
        ContactThanks.as_view()),

    url(r'^categories/(?P<category>[-\w]+)/$',
        CategoriesListView.as_view(),
        name='category'),

    url(r'^posts/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/$',
        PostDetailView.as_view(),
        name='post'),

    url(r'^posts/(?P<year>\d{4})/(?P<month>\d{1,2})/$',
        PostMonthArchiveView.as_view(),
        name='archive_month'),

    (r'^posts/$',
        RedirectView.as_view(url='/')),

    (r'^categories/$',
        RedirectView.as_view(url='/')),

    # TOFIX 
    (r'^robots\.txt$',
        RedirectView.as_view(url=settings.STATIC_URL + 'robots.txt')),
)

sitemaps = {
    'posts': PostsSitemap(),
    'flatpages': FlatPageSitemap,
    'categories': CategoriesSitemap()
}

urlpatterns += patterns('django.contrib.sitemaps.views',
    (r'^sitemap\.xml$', 'sitemap', {
        'sitemaps': sitemaps,
        'template_name': 'sitemap.xml'
    }),
)
