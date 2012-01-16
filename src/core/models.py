from django.db import models
from django.db.models import permalink
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django.template.defaultfilters import slugify


class Category(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)

    def __unicode__(self):
        return self.title

    def save(self):
        self.slug = slugify(self.title)
        super(Category, self).save()

    @permalink
    def get_absolute_url(self):
        return ('category', [self.slug])


class Post(models.Model):
    title = models.CharField(max_length=50)
    slug = models.CharField(max_length=50)
    excerpt = models.CharField(max_length=140)
    content = models.TextField()
    is_draft = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField()

    user = models.ForeignKey(User)
    category = models.ManyToManyField(Category)

    def __unicode__(self):
        return self.title

    def save(self):
        self.slug = slugify(self.title)
        super(Post, self).save()

    @permalink
    def get_absolute_url(self):
        y = self.published_date.strftime('%Y')
        m = self.published_date.strftime('%m')
        d = self.published_date.strftime('%d')
        return ('post', None, {'year': y, 'month': m, 'day': d, 'slug': self.slug})

    class Meta:
        ordering = ['-published_date']
