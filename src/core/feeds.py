from django.contrib.syndication.views import Feed
from core.models import Post

class PostsFeed(Feed):
	title = 'Feed'
	link = '/posts/'
	description = 'posts'
	
	def items(self):
		return Post.objects.filter(is_draft=False)
		
	def item_title(self, item):
		return item.title
	
	def item_description(self, item):
		return item.excerpt
