from django.contrib.auth.tokens import PasswordResetTokenGenerator


class UserTokenActivation(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return f"{user.pk}{user.password}{user.is_active}{timestamp}"


user_token_activation = UserTokenActivation()
