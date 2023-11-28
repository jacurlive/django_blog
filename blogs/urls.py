from django.contrib.auth.views import LogoutView
from django.urls import path, reverse_lazy

from blogs.views import home_view, blog_view, about_view, post_view, custom_login_view, register_view, CreateBlogView, \
    profile_view, change_password_view, activate_account, contact_view


urlpatterns = [
    path('', home_view, name='main'),
    path('blogs', blog_view, name='blogs'),
    path('about', about_view, name='about'),
    path('blog/<str:slug>', post_view, name='post_detail'),
    path('login', custom_login_view, name='login'),
    path('logout', LogoutView.as_view(next_page=reverse_lazy('main')), name='logout'),
    path('signup', register_view, name='register'),
    path('activate/<str:uidb64>/<str:token>/', activate_account, name='activate'),
    path('add', CreateBlogView.as_view(), name='add'),
    path('profile', profile_view, name='profile'),
    path('change_password', change_password_view, name='change_password'),
    path('contact', contact_view, name='contact')
    ]
