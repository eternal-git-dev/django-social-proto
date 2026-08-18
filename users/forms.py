from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser


class BaseUserForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control',
            }
        ),
        required=False,
    )

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


class RegistrationForm(UserCreationForm, BaseUserForm):

    class Meta(BaseUserForm.Meta):
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'avatar',
            'bio',
            'date_of_birth',
        )


class ProfileUpdateForm(BaseUserForm):
    pass