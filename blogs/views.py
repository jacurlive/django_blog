from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, FormView, UpdateView

from blogs.forms import LoginForm, RegisterForm, ProfileForm
from blogs.models import Blog, Category, User, AboutUs


class HomeView(ListView):
    queryset = Blog.objects.filter(status='active').order_by('-created_at')[1:]
    template_name = 'blogs/index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['last'] = Blog.objects.filter(status='active').last()
        context['categories'] = Category.objects.all()
        return context


class BlogView(ListView):
    queryset = Blog.objects.filter(status='active').order_by('-created_at')
    template_name = 'blogs/blog-category.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        slug = self.request.GET.get('category')
        qs = self.get_queryset()
        context['trending_posts'] = Blog.objects.order_by('-created_at')
        context['posts'] = qs
        context['category_slug'] = Category.objects.filter(slug=slug).first()
        context['categories'] = Category.objects.all()
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        if category := self.request.GET.get('category'):
            return qs.filter(category__slug=category)
        return qs


class AboutView(ListView):
    template_name = 'blogs/about.html'
    queryset = AboutUs.objects.first()
    context_object_name = 'about'


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
    success_url = reverse_lazy('confirm_email')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class ConfirmEmailView(TemplateView):
    template_name = 'auth/confirm_email.html'


class CreateBlogView(TemplateView):
    template_name = 'blogs/add-post.html'


class ProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'profile/profile.html'
    queryset = User.objects.all()
    form_class = ProfileForm
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user

    def get(self, request, **kwargs):
        if self.request.user.is_anonymous:
            return redirect('login')
        self.object = self.request.user
        context = self.get_context_data(object=self.object, form=self.form_class)
        return self.render_to_response(context)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
    def form_invalid(self, form):
        print(1)
        return super().form_invalid(form)


class ChangePasswordView(TemplateView):
    template_name = 'profile/change_password.html'

