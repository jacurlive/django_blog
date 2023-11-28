from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import make_password
from django.forms import ModelForm, Form, CharField, EmailField, Textarea
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from blogs.models import User, Blog
from django import forms


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'description', 'image', 'category']


class LoginForm(AuthenticationForm):
    pass


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    def clean_password(self):
        password = self.data.get('password1')
        print(self.data)
        confirm_password = self.data.get('password2')
        if password != confirm_password:
            print('password error')
            raise forms.ValidationError('Check your password')
        return make_password(password)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'password1']


class ProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'phone', 'bio', 'image']


class ChangePasswordForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ['password']


class ContactForm(Form):
    name = CharField(max_length=100)
    email = EmailField()
    website = CharField(required=False)
    message = CharField(widget=Textarea)
