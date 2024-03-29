from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.urls import reverse
from django.utils.html import format_html
from blogs.models import Blog, Category, Comment, AboutUs, ContactMessage, User


@admin.register(User)
class UserAdmin(ModelAdmin):
    list_display = ('username', 'is_staff', 'email', 'is_active')
    list_editable = ('is_active',)


@admin.register(Blog)
class BlogsAdmin(ModelAdmin):
    search_fields = ('title', 'status')
    fields = ('title', 'description', 'image', 'category', 'status', 'user')
    list_display = ('id', 'title', 'status', 'categories')
    list_display_links = ('title',)
    list_editable = ('status',)

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


@admin.register(ContactMessage)
class ContactMessageAdmin(ModelAdmin):
    list_display = ('name', 'email', 'website', 'message')
