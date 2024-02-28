from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from typing import Any
from django.urls import reverse
from django.utils.text import slugify
from django.db.models import Sum

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .models import (
    CategoryArticlesModel,
    TagArticlesModel,
    ArticlesModel,
)

from .forms import (
    CreateArticleForm,
    UpdateArticleForm,
    )

class ArticlesListView(ListView):
    model = ArticlesModel
    template_name = 'templates_articles/articles_list.html'
    ordering = ['-date_created']
    paginate_by = 6
    context_object_name = 'articles'

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["publicacoes_count"] = ArticlesModel.objects.all().count()
        context["hide_sidebar"] = True
        return context


class ArticleSingleView(DetailView):
    model = ArticlesModel
    template_name = 'templates_articles/article_single.html'
    slug_field = 'slug'
    reverse_lazy = reverse_lazy('article-delete-post')
    context_object_name = 'articles'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Contagem das Visualizações
        self.object.update_views() 
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['categories'] = CategoryArticlesModel.objects.all()
        context['tagsx'] = TagArticlesModel.objects.all()
        articles = self.get_object()
        context['tags'] = articles.tags.all()
        context['current_app'] = 'app_articles'
        return context


class CategoryListView(ListView):
    model = CategoryArticlesModel
    template_name = 'templates_articles/categories.html'
    context_object_name = 'articles'
    
    def get_queryset(self):
        category_slug = self.kwargs['category_slug']
        category = CategoryArticlesModel.objects.get(slug=category_slug)
        return ArticlesModel.objects.filter(category=category)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs['category_slug']
        context['category'] = CategoryArticlesModel.objects.get(slug=category_slug)
        context['categories'] = CategoryArticlesModel.objects.all()
        context['tagsx'] = TagArticlesModel.objects.all()
        context['current_app'] = 'app_articles'
        return context


class TagArticlesView(ListView):
    model = TagArticlesModel
    template_name = 'templates_articles/article_tags.html'
    context_object_name = 'articles'

    def get_queryset(self):
        tagArticle_slug = self.kwargs['tagArticle_slug']
        tags = get_object_or_404(TagArticlesModel, slug=tagArticle_slug)
        return ArticlesModel.objects.filter(tags=tags)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        tagArticle_slug = self.kwargs['tagArticle_slug']
        context['tags'] = get_object_or_404(TagArticlesModel, slug=tagArticle_slug)
        context['categories'] = CategoryArticlesModel.objects.all()
        context ['tagsx'] = TagArticlesModel.objects.all()
        context['current_app'] = 'app_articles'
        return context

# Classes Create; Update Articles

class CreateArticleView(CreateView):
    model = ArticlesModel
    template_name = 'templates_articles/article_create_post.html'
    form_class = CreateArticleForm
    success_url = reverse_lazy('app_articles:article-single')  # Ajuste conforme a URL de sucesso desejada

    def form_valid(self, form):
        form.instance.slug = slugify(form.instance.title)
        response = super(CreateArticleView, self).form_valid(form)
        return response
    
    def get_success_url(self):
        return reverse('app_articles:article-single', kwargs={'slug': self.object.slug})
    
class UpdateArticleView(UpdateView):
    model = ArticlesModel
    form_class = UpdateArticleForm
    template_name = 'templates_articles/article_update_post.html'
    success_url = reverse_lazy('app_articles:articles-list')

class DeleteArticleView(DeleteView):
    model = ArticlesModel
    template_name = 'templates_articles/article_delete_post.html'
    success_url = reverse_lazy('app_articles:articles-list')
    
