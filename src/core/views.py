from django.db.models import Q
from django.contrib import messages
from django.core.mail import send_mail
from django.views.generic import ListView, DetailView, FormView, TemplateView
from django.views.generic.dates import MonthArchiveView

import calendar

from core.models import Category, Post
from core.forms import ContactForm

class PostSearch(ListView):
    queryset = Post.objects.none()
    paginate_by = 4
    template_name = 'core/post_list.html'

    def get_queryset(self):
        q = self.request.GET.get('q', False)
        if q and len(q) >= 3:
            q = q.strip()
            self.queryset = Post.objects.filter(Q(title__icontains=q) | Q(excerpt__icontains=q) | Q(content__icontains=q))

        if self.queryset:
            messages.info(self.request, 'Resultados para: <em>%s</em>' % q)
        else:
            messages.error(self.request, 'Desculpe, nada retornou nesta busca. Por favor, tente novamente com palavras-chave diferentes.')

        return self.queryset

    def get_context_data(self, **kwargs):
        context = super(PostSearch, self).get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', False)
        context['title'] = 'Busca: %s' % self.request.GET.get('q', False)

        return context

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
        year = self.kwargs['year']
        month = calendar.month_name[int(self.kwargs['month'])]

        context = super(PostMonthArchiveView, self).get_context_data(**kwargs)
        context['title'] = '%s %s' % (month, year)
        messages.info(self.request, 'Arquivos Mensais: <em>%s %s</em>' % (month, year))

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
        category = Category.objects.get(slug=self.kwargs['category'])

        context = super(CategoriesListView, self).get_context_data(**kwargs)
        context['title'] = category
        messages.info(self.request, 'Arquivos da Categoria: <em>%s</em>' % category)

        return context

class Contact(FormView):
    form_class = ContactForm
    success_url = '/pages/contact/thanks'
    template_name = 'core/contact.html'

    def form_valid(self, form):
        data = form.cleaned_data
        send_mail('Contato: %s' % data['name'], data['message'], 'leandrotoledo@members.fsf.org', [data['sender']], fail_silently=True)

        return super(Contact, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(Contact, self).get_context_data(**kwargs)
        context['title'] = 'Contato'

        return context

class ContactThanks(TemplateView):
    template_name = 'core/contact_thanks.html'

    def get_context_data(self, **kwargs):
        context = super(ContactThanks, self).get_context_data(**kwargs)
        context['title'] = 'Contato: Obrigado'

        return context
