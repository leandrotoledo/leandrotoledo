from django.db.models import Count
from core.models import Category, Post

def archives(request):
    return {'archives': Post.objects.filter().dates('published_date', 'month')}

def categories(request):
    return {'categories': Category.objects.annotate(Count('post')).order_by('title')}

