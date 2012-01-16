from django.db.models import Count
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from core.models import Category, Post

def site(request):
    return {'site': Site.objects.get_current()}

def author(request):
    return {'author': User.objects.filter(is_staff=True)[0]}

def archives(request):
    return {'archives': Post.objects.filter(is_draft=False).dates('published_date', 'month')}

def categories(request):
    return {'categories': Category.objects.annotate(Count('post')).order_by('title')}
