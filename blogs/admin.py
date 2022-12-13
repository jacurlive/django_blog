from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.urls import reverse
from django.utils.html import format_html

from blogs.models import Blog, Category, Comment, AboutUs


@admin.register(Blog)
class BlogsAdmin(ModelAdmin):
    search_fields = ('title',)
    fields = ('title', 'description', 'image', 'category', 'user')
    list_display = ('id', 'title', 'categories')

    def categories(self, obj):
        lst = []
        for i in obj.category.all():
            lst.append(f'''<a href="{reverse('admin:blogs_category_change', args=(i.pk,))}">{i.name}</a>''')
        return format_html(', '.join(lst))


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    search_fields = ('name',)
    list_display = ('name',)
    exclude = ('slug',)

    @staticmethod
    def blog_count(obj):
        return obj.blog_set.count()


@admin.register(Comment)
class CommentsAdmin(ModelAdmin):
    search_fields = ('text',)
    fields = ('text', 'user', 'blog')


@admin.register(AboutUs)
class AboutUsAdmin(ModelAdmin):
    list_display = ('about', 'phone', 'email', 'address')
