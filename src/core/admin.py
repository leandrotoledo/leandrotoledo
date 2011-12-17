from core.models import Category, Post
from django.contrib import admin

class PostAdmin(admin.ModelAdmin):
	fieldsets = (
		(None, {
			'fields': ('title', 'excerpt', 'content', 'published_date')
		}),
	)
	
	def save_model(self, request, obj, form, change):
		obj.user = request.user
		obj.save()
 
admin.site.register(Post, PostAdmin)
admin.site.register(Category)
