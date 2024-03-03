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
from django.http import HttpRequest, HttpResponse
from django.utils import timezone
from app_manager .models import PageView

from .forms import (
    BlogCreateForm,
    BlogUpdateForm,
)

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .models import (
    CategoryBlogSocialModel,
    TagBlogSocialModel,
    BlogSocialModel,
)

class BlogSocialListView(ListView):
    model = BlogSocialModel
    template_name = 'templates_blog_social/blog_social_list.html'
    ordering = ['-date_created']
    paginate_by = 6
    context_object_name = 'blog'
    
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["publicacoes_count"] = BlogSocialModel.objects.all().count()
        context["hide_sidebar"] = True
        return context

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        page, created = PageView.objects.get_or_create(
            page_name="Lista de Artigos Blog-Social",
            defaults={'last_accessed': timezone.now()}
        )
        if not created:
            page.view_count += 1
            page.last_accessed = timezone.now()
            page.save()

        return super().get(request, *args, **kwargs)

class BlogSocialSingleView(DetailView):
    model = BlogSocialModel
    template_name = 'templates_blog_social/blog_social_single.html'
    slug_field = 'slug'
    context_object_name = 'blog'
    reverse_lazy = reverse_lazy('blog-social-delete-post')
    
    
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        self.object = self.get_object()
        articleBlog_name = self.object.title
        self.object.update_views()

        page, created = PageView.objects.get_or_create(
            page_name=f"Blog-Social Post Post: {articleBlog_name}",
            defaults={'last_accessed': timezone.now()}
        )
        if not created:
            page.view_count += 1
            page.last_accessed = timezone.now()
            page.save()

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)
    
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['categories'] = CategoryBlogSocialModel.objects.all()
        context['tagsx'] = TagBlogSocialModel.objects.all()
        context['category'] = CategoryBlogSocialModel.objects.all()
        blog = self.get_object()
        context['tags'] = blog.tags.all()
        context['current_app'] = 'app_blog_social'
        return context
    
class CategoryBlogSocialView(ListView):
    model = CategoryBlogSocialModel
    template_name = 'templates_blog_social/blog_social_categories.html'
    context_object_name = 'blog'
    
    def get_queryset(self):
        self.category = CategoryBlogSocialModel.objects.get(slug=self.kwargs['category_social_slug'])
        return BlogSocialModel.objects.filter(category=self.category)
    
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update({
            'category': self.category,
            'categories':  CategoryBlogSocialModel.objects.all(),
            'tagsx': TagBlogSocialModel.objects.all(),
            "tag": TagBlogSocialModel.objects.all(),
            'current_app': 'app_blog_social',
        })
        return context
    
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        page, created = PageView.objects.get_or_create(
            page_name=f"Blog: Categorias - {self.kwargs.get('category_social_slug', 'Unknown')}",
            defaults={'last_accessed': timezone.now()}
        )
        if not created:
            page.view_count += 1
            page.last_accessed = timezone.now()
            page.save()

        return super().get(request, *args, **kwargs)

class TagBlogSocialView(ListView):
    model = TagBlogSocialModel
    template_name = 'templates_blog_social/blog_social_tags.html'
    context_object_name = 'blog'
    
    def get_queryset(self):
        self.tag = get_object_or_404(TagBlogSocialModel, slug=self.kwargs['tagBlogSocial_slug'])
        return BlogSocialModel.objects.filter(tags=self.tag)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update({
            'tag': TagBlogSocialModel.objects.all(),
            'category': CategoryBlogSocialModel.objects.all(),
            'categories': CategoryBlogSocialModel.objects.all(),
            'tagsx': TagBlogSocialModel.objects.all(),
            'current_app': 'app_blog_social',
        })
        return context

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        page, created = PageView.objects.get_or_create(
            page_name=f"Blog Social: Tags - {self.kwargs.get('tagBlogSocial_slug', 'Unknown')}",
            defaults={'last_accessed': timezone.now()}
        )
        if not created:
            page.view_count += 1
            page.last_accessed = timezone.now()
            page.save()

        return super().get(request, *args, **kwargs)

# Classes Create

class CreateBlogPostView(CreateView):
    model = BlogSocialModel
    template_name = 'templates_blog_social/blog_create_post.html'
    form_class = BlogCreateForm
    
    def form_valid(self, form):
        form.instance.slug = slugify(form.instance.title)
        response = super(CreateBlogPostView, self).form_valid(form)
        return response
    
    def get_success_url(self):
        return reverse('app_blog_social:blog-social-single', kwargs={'slug': self.object.slug})
    
    
class UpdateBlogView(UpdateView):
    model = BlogSocialModel
    form_class = BlogUpdateForm
    template_name = 'templates_blog_social/blog_update_post.html'
    success_url = reverse_lazy('app_blog_social:blog-social-list')

class DeleteBlogView(DeleteView):
    model = BlogSocialModel
    template_name = 'templates_blog_social/blog_delete_post.html'
    success_url = reverse_lazy('app_blog_social:blog-social-list')
    