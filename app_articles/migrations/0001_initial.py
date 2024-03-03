# Generated by Django 5.0.2 on 2024-03-03 02:19

import ckeditor_uploader.fields
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryArticlesModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('slug', models.SlugField()),
            ],
        ),
        migrations.CreateModel(
            name='TagArticlesModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('slug', models.SlugField()),
            ],
        ),
        migrations.CreateModel(
            name='ArticlesModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('img_destaque', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True)),
                ('meta_description', models.TextField(max_length=250)),
                ('keyword', models.CharField(max_length=255)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('is_published', models.BooleanField(default=True)),
                ('old_url', models.SlugField(blank=True, null=True)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('code', models.PositiveIntegerField(blank=True, null=True, unique=True)),
                ('views', models.IntegerField(default=0)),
                ('author', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_articles.categoryarticlesmodel')),
                ('tags', models.ManyToManyField(blank=True, to='app_articles.tagarticlesmodel')),
            ],
        ),
    ]
