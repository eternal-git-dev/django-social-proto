from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from posts.views import PostListView

urlpatterns = [
    path('', PostListView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('posts/', include('posts.urls')),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
