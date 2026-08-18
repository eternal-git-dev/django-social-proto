from django.urls import path

from .views import (
    ProfileEditView,
    ProfileView,
    RegistrationView,
    UserLoginView,
    UserLogoutView,
)

app_name = 'users'


urlpatterns = [
    path('register/', RegistrationView.as_view(), name='registration'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path(
        'profile/edit/',
        ProfileEditView.as_view(),
        name='profile_edit',
    ),
    path(
        '<slug:username>/',
        ProfileView.as_view(),
        name='profile',
    ),
]
