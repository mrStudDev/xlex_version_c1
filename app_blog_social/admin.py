from django.contrib import admin

from .models import (
    CategoryBlogSocialModel,
    TagBlogSocialModel,
    BlogSocialModel,
    )


class BlogSocialAdmin(admin.ModelAdmin):
    list_display = ["__str__", "date_created"]
    list_filter = ["date_created"]
    search_fields = ["title"]
    prepopulated_fields = {"slug": ("title",)}
    
    class Meta:
        model = BlogSocialModel

       
class CategorySocialAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

    class Meta:
        model = CategoryBlogSocialModel


class TagBlogSocialAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    
    class Meta:
        model = TagBlogSocialModel

    

admin.site.register(BlogSocialModel, BlogSocialAdmin)
admin.site.register(CategoryBlogSocialModel, CategorySocialAdmin)
admin.site.register(TagBlogSocialModel, TagBlogSocialAdmin)
