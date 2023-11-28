from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.contrib.sites.shortcuts import get_current_site
from django.views.generic import View
from django.core.mail import EmailMessage
from blogs.forms import LoginForm, RegisterForm, ProfileForm, ChangePasswordForm, BlogForm, ContactForm
from blogs.models import Blog, Category, User, AboutUs, ContactMessage
from django.contrib.auth import login, update_session_auth_hash
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.utils.safestring import mark_safe
from .tokens import account_activation_token


def activate_account(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None

    if user is not None:
        user.is_active = True
        user.save()
        login(request, user)
        return render(request, 'auth/account_activation_success.html')
    else:
        return render(request, 'auth/account_activation_failure.html')


def home_view(request):
    queryset = Blog.objects.filter(status='active').order_by('-created_at')[1:]
    last_post = Blog.objects.filter(status='active').last()
    categories = Category.objects.all()

    context = {
        'blog_list': queryset,
        'last': last_post,
        'categories': categories,
    }

    return render(request, 'blogs/index.html', context)


def blog_view(request):
    queryset = Blog.objects.filter(status='active').order_by('-created_at')
    slug = request.GET.get('category')
    qs = queryset.filter(category__slug=slug) if slug else queryset

    context = {
        'posts': qs,
        'trending_posts': Blog.objects.order_by('-created_at'),
        'category_slug': Category.objects.filter(slug=slug).first(),
        'categories': Category.objects.all(),
    }

    return render(request, 'blogs/blog-category.html', context)


def about_view(request):
    about_us = AboutUs.objects.first()

    context = {
        'about': about_us,
    }

    return render(request, 'blogs/about.html', context)


def post_view(request, slug):
    post = Blog.objects.get(slug=slug)
    categories = Category.objects.filter(blog=post)
    users = User.objects.all()

    context = {
        'post': mark_safe(post),
        'categories': categories,
        'user': users,
    }

    return render(request, 'blogs/post.html', context)


def custom_login_view(request):
    form_class = LoginForm
    template_name = 'auth/login.html'
    next_page = reverse_lazy('main')

    login_view = LoginView.as_view(form_class=form_class, template_name=template_name, success_url=next_page)

    return login_view(request)


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('auth/confirm_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.content_subtype = 'html'
            email.send()

            return render(request, 'auth/registration_confirmation.html')
        else:
            print(form.errors)
    else:
        form = RegisterForm()

    return render(request, 'auth/register.html', {'form': form})


def about_view(request):
    template_name = 'blogs/about.html'
    context = {'about': AboutUs.objects.first()}

    return render(request, template_name, context)


def post_view(request, slug):
    template_name = 'blogs/post.html'
    post = Blog.objects.get(slug=slug)
    categories = Category.objects.filter(blog=post)
    users = User.objects.all()

    context = {
        'post': post,
        'categories': categories,
        'user': users,
    }

    return render(request, template_name, context)


def profile_view(request):
    template_name = 'profile/profile.html'
    form_class = ProfileForm
    success_url = reverse_lazy('profile')

    user = request.user

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect(success_url)
    else:
        form = form_class(instance=user)

    context = {'object': user, 'form': form}

    return render(request, template_name, context)


def change_password_view(request):
    template_name = 'profile/change_password.html'
    form_class = ChangePasswordForm
    success_url = reverse_lazy('profile')

    user = request.user

    if request.method == 'POST':
        form = form_class(user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)  # Обновить хеш сессии, чтобы пользователь не был разлогинен
            return redirect(success_url)
    else:
        form = form_class(user)

    context = {'form': form}

    return render(request, template_name, context)


class CreateBlogView(View):
    template_name = 'blogs/add-post.html'

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        form = BlogForm()
        return render(request, self.template_name, {'form': form, 'categories': categories})

    def post(self, request, *args, **kwargs):
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.user = request.user
            blog.save()
            form.save_m2m()
            return redirect('main')
        else:
            print(form.errors)
            categories = Category.objects.all()
            return render(request, self.template_name, {'form': form, 'categories': categories})


def contact_view(request):
    template_name = 'blogs/contact.html'
    about = AboutUs.objects.first()
    # success_page = reverse_lazy('main')

    context = {
        'about': about
    }

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = ContactMessage(
                name = form.cleaned_data['name'],
                email = form.cleaned_data['email'],
                website = form.cleaned_data['website'],
                message = form.cleaned_data['message']
            )
            contact_message.save()

            messages.success(request, 'Your message was sent successfully')

            return redirect('contact')
        else:
            form = ContactForm()


    return render(request, template_name, context)
