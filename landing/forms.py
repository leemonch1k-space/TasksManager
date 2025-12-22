from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from task.models import Position


User = get_user_model()


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    position = forms.ModelChoiceField(
        queryset=Position.objects.all(),
        empty_label="Choose your position",
        required=True
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + (
            "email",
            "position",
            "first_name",
            "last_name",
        )
