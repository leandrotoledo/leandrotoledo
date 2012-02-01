from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, RedirectView
from django.views.generic.dates import MonthArchiveView

from core.models import Category, Post

class PostsListView(ListView):
    queryset = Post.objects.filter(is_draft=False)
    paginate_by = 4

    def get_queryset(self):
        if self.request.user.is_staff == True:
            self.queryset = Post.objects.all()
        return self.queryset

class PostDetailView(DetailView):
    model = Post

class PostMonthArchiveView(MonthArchiveView):
    model = Post
    date_field = 'published_date'
    month_format= '%m'

class CategoriesListView(ListView):
    model = Category
