from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.forms import ModelForm, CharField, PasswordInput

import blogs.models
from blogs.models import User


class LoginForm(AuthenticationForm):
    pass


class RegisterForm(ModelForm):
    confirm_password = CharField(widget=PasswordInput(attrs={"autocomplete": "current-password"}),)

    def clean_password(self):
        password = self.data.get('password')
        confirm_password = self.data.get('confirm_password')
        if password != confirm_password:
            raise ValidationError('Check you password')
        return make_password(password)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'password']
