from django.contrib.syndication.views import Feed
from django.contrib.sites.models import Site
from core.models import Post

class PostsFeed(Feed):
	title = Site.objects.get_current().name
	link = '/'
	description = Site.objects.get_current().sitedetail.description
	
	def items(self):
		return Post.objects.filter(is_draft=False)
		
	def item_title(self, item):
		return item.title
	
	def item_description(self, item):
		return item.excerpt
