from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, FormView

from blogs.forms import LoginForm, RegisterForm
from blogs.models import Blog, Category, User


class HomeView(ListView):
    queryset = Blog.objects.order_by('-created_at')[1:]
    template_name = 'blogs/index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['last'] = Blog.objects.last()
        context['categories'] = Category.objects.all()
        return context


class BlogView(ListView):
    queryset = Blog.objects.order_by('-created_at')
    template_name = 'blogs/blog-category.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['categories'] = Category.objects.all()
        return context


class AboutView(TemplateView):
    template_name = 'blogs/about.html'


class PostView(DetailView):
    template_name = 'blogs/post.html'
    query_pk_and_slug = 'slug'
    queryset = Blog.objects.all()
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(blog=context['post'])
        context['user'] = User.objects.all()
        return context


class CustomLoginView(LoginView):
    template_name = 'auth/login.html'
    form_class = LoginForm
    next_page = reverse_lazy('main')


class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'auth/register.html'
    success_url = reverse_lazy('main')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class ConfirmEmailView(TemplateView):
    template_name = 'auth/confirm_email.html'
