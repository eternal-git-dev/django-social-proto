from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse
from django.views.generic import CreateView, DetailView, UpdateView

from users.forms import ProfileUpdateForm, RegistrationForm
from users.models import CustomUser


class UserProfileRedirectMixin:
    def get_success_url(self):
        return reverse(
            'users:profile',
            kwargs={'username': self.object.username},
        )


class ProfileView(DetailView):
    model = CustomUser
    template_name = 'users/profile.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    context_object_name = 'profile'


class ProfileEditView(
    LoginRequiredMixin,
    UserProfileRedirectMixin,
    UpdateView,
):
    model = CustomUser
    form_class = ProfileUpdateForm
    template_name = 'users/profile_form.html'

    def get_object(self):
        return self.request.user


class RegistrationView(
    UserProfileRedirectMixin,
    CreateView,
):
    model = CustomUser
    template_name = 'users/registration.html'
    form_class = RegistrationForm


class UserLoginView(LoginView):
    form_class = AuthenticationForm
    template_name = 'users/login.html'


class UserLogoutView(LogoutView):
    next_page = 'users:login'
