from django.contrib.sitemaps import Sitemap
from core.models import Category, Post

class CategoriesSitemap(Sitemap):
    changefreq = 'never'
    priority = 0.3

    def items(self):
        return Category.objects.filter(post__is_draft=False).distinct()

class PostsSitemap(Sitemap):
    changefreq = 'never'
    priority = 0.5

    def items(self):
        return Post.objects.filter(is_draft=False)

    def lastmod(self, obj):
        return obj.published_date
