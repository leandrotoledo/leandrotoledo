from core.models import Category, Post, UserProfile, SiteDetail
from django.contrib import admin


class PostAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('title', 'excerpt', 'content', 'category', 'is_draft', 'published_date')
        }),
    )

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()


class CategoryAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('title',)
        }),
    )


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(UserProfile)
admin.site.register(SiteDetail)
