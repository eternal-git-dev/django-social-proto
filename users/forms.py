from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser


class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'avatar',
            'bio',
            'date_of_birth',
        )


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = (
            'first_name',
            'last_name',
            'email',
            'avatar',
            'bio',
            'date_of_birth',
        )
