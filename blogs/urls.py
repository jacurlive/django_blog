from django.contrib.auth.views import LogoutView
from django.urls import path, reverse_lazy

from blogs.views import HomeView, BlogView, AboutView, PostView, CustomLoginView, RegisterView, ConfirmEmailView, \
    CreateBlogView, ProfileView, ChangePasswordView

urlpatterns = [
    path('', HomeView.as_view(), name='main'),
    path('blogs', BlogView.as_view(), name='blogs'),
    path('about', AboutView.as_view(), name='about'),
    path('blog/<str:slug>', PostView.as_view(), name='post_detail'),
    path('login', CustomLoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(next_page=reverse_lazy('main')), name='logout'),
    path('signup', RegisterView.as_view(), name='register'),
    path('confirm_email', ConfirmEmailView.as_view(), name='confirm_email'),
    path('add', CreateBlogView.as_view(), name='add'),
    path('profile', ProfileView.as_view(), name='profile'),
    path('change_password', ChangePasswordView.as_view(), name='change_password')
    ]
