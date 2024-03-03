from django.urls import path
from . views import (
    BlogSocialListView,
    BlogSocialSingleView,
    CategoryBlogSocialView,
    TagBlogSocialView,
    CreateBlogPostView,
    UpdateBlogView,
    DeleteBlogView,
)

app_name = 'app_blog_social'

urlpatterns = [
    path('', BlogSocialListView.as_view(), name='blog-social-list'),
    path('blog-post/<slug:slug>', BlogSocialSingleView.as_view(), name='blog-social-single'),
    path('categorias/<slug:category_social_slug>/', CategoryBlogSocialView.as_view(), name='blog-social-categories'),
    path('tags-blog-social/<slug:tagBlogSocial_slug>/', TagBlogSocialView.as_view(), name='blog-social-tag'),
    path('blog-create-post/', CreateBlogPostView.as_view(), name='blog-social-create'),
    path('blog-update-post/<slug:slug>/', UpdateBlogView.as_view(), name='blog-update-post'),
    path('blog-delete/<slug:slug>/', DeleteBlogView.as_view(), name='blog-delete-post'),

]