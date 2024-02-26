from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse
import random
from django.utils.text import slugify


class CategoryArticlesModel(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    slug = models.SlugField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('app_home:home-view')

class TagArticlesModel(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    slug = models.SlugField()

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('app_home:home-view')


class ArticlesModel(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    img_destaque = models.ImageField(upload_to='images/', null=True, blank=True)
    category = models.ForeignKey(CategoryArticlesModel, null=True, blank=True, on_delete=models.SET_NULL)
    content = RichTextUploadingField(blank=True, null=True)
    meta_description = models.TextField(max_length=250)
    keyword = models.CharField(max_length=255)
    tags = models.ManyToManyField('TagArticlesModel', blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)
    old_url = models.SlugField(blank=True, null=True)
    slug = models.SlugField(blank=True, unique=True)
    last_updated = models.DateTimeField(auto_now=True)
    code = models.PositiveIntegerField(unique=True, blank=True, null=True)
    views = models.IntegerField(default=0)  


    def generate_unique_code(self):
        code = random.randint(100000, 999999)
        while ArticlesModel.objects.filter(code=code).exists():
            code = random.randint(100000, 999999)
        return code

    def save(self, *args, **kwargs):
        # Gera um código único se não existir
        if not self.code:
            self.code = self.generate_unique_code()
        # Gera um slug a partir do título se o slug não existir
        if not self.slug:
            self.slug = slugify(self.title)
        super(ArticlesModel, self).save(*args, **kwargs)


    def __str__(self):
        return f"{self.title} | {self.author} | {self.views}"


    def get_absolute_url(self):
        return reverse('app_articles:article-single', kwargs={'slug': self.slug})

    def update_views(self, *args, **kwargs):
         self.views = self.views + 1
         super(ArticlesModel, self).save(*args, **kwargs)