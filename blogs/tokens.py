from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp) -> str:
        return f"{user.pk}{user.is_active}{timestamp}"


account_activation_token = AccountActivationTokenGenerator()
