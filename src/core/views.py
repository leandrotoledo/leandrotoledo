from django.contrib import messages
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
    paginate_by = 4
    month_format = '%m'
    template_name = 'core/post_list.html'

    def get_context_data(self, **kwargs):
        context = super(PostMonthArchiveView, self).get_context_data(**kwargs)
        messages.info(self.request, 'Arquivos Mensais: <em>%s</em>' % self.request.user)
        return context

class CategoriesListView(ListView):
    model = Category
    paginate_by = 4
    template_name = 'core/post_list.html'

    def get_queryset(self):
        category = self.kwargs['category']
        self.queryset = Post.objects.filter(category__slug=category)
        return self.queryset

    def get_context_data(self, **kwargs):
        context = super(CategoriesListView, self).get_context_data(**kwargs)
        messages.info(self.request, 'Arquivos da Categoria: <em>%s</em>' % self.request.user)
        return context
