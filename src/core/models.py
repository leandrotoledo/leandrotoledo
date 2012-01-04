from django.db import models
from django.db.models import permalink
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
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
    title = models.CharField(max_length=65)
    slug = models.CharField(max_length=65)
    excerpt = models.CharField(max_length=150)
    content = models.TextField()
    # is_draft = models.BooleanField(default=True)
    published = models.BooleanField()
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


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    google_profile = models.CharField(max_length=50)


class SiteDetail(models.Model):
    site = models.OneToOneField(Site)
    keywords = models.CharField(max_length=150)
    description = models.CharField(max_length=150)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
post_save.connect(create_user_profile, sender=User)
