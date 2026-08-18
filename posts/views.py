from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from django.views.generic import DeleteView, DetailView, ListView, UpdateView
from django.views.generic.edit import CreateView

from .forms import PostForm
from .models import Post

POSTS_PER_PAGE = 10


class PostAuthorMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.get_object().author == self.request.user


class PostFormMixin:
    model = Post
    form_class = PostForm
    template_name = 'posts/post_form.html'

    def get_success_url(self):
        return reverse(
            'posts:post_detail',
            kwargs={'post_id': self.object.pk},
        )


class PostCreateView(
    LoginRequiredMixin,
    PostFormMixin,
    CreateView,
):
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostListView(ListView):
    model = Post
    template_name = 'posts/post_list.html'
    paginate_by = POSTS_PER_PAGE

    def get_queryset(self):
        return Post.objects.select_related('author').order_by('-created_at')


class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    pk_url_kwarg = 'post_id'


class PostUpdateView(
    PostAuthorMixin,
    PostFormMixin,
    UpdateView,
):
    pk_url_kwarg = 'post_id'


class PostDeleteView(
    PostAuthorMixin,
    DeleteView,
):
    model = Post
    template_name = 'posts/post_confirm_delete.html'
    pk_url_kwarg = 'post_id'

    def get_success_url(self):
        return reverse('posts:post_list')
