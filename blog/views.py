from django.shortcuts import redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from .models import Post
from .forms import PostForm, CommentForm
from .tasks import send_mail_task


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'blog/list.html'

    def get_queryset(self):
        queryset = super(PostListView, self).get_queryset()
        author_name = self.request.GET.get('author')
        if author_name:
            queryset = queryset.filter(author__username=author_name)
        return queryset

    def get_context_data(self, **kwargs):
        author_name = self.request.GET.get('author')
        context = super().get_context_data(**kwargs)
        if author_name:
            context['author'] = author_name
        return context


class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'blog/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostEditView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blog:post-list')


class CommentCreateView(View):

    @method_decorator(login_required)
    def post(self, request, pk):
        form = CommentForm(request.POST)
        if form.is_valid():
            post = get_object_or_404(Post, pk=pk)
            form.instance.post = post
            form.instance.author = request.user
            form.save()
            if request.user != post.author:
                message = render_to_string(
                    'account/new_comment_email.html',
                    {
                        'author': post.author.username,
                        'user': request.user.username,
                        'post': post,
                        'domain': get_current_site(request).domain,
                        'comment': form.cleaned_data.get('text'),
                    }
                )
                send_mail_task.delay(
                    subject='New comment',
                    message=message,
                    to_email=post.author.email
                )
            return redirect('blog:post-detail', post.pk)
