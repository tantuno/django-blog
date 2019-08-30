from django.shortcuts import get_object_or_404,redirect
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.utils.decorators import method_decorator
from django.core.mail import EmailMessage
from django.urls import reverse_lazy
from .models import Post, Comment
from .forms import PostForm, CommentForm
from .tasks import send_mail_task, adding_task

class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'blog/list.html'


class UserPostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'blog/list.html'

    def get_queryset(self):
        user = get_object_or_404(get_user_model(), username=self.kwargs.get('username'))
        return Post.objects.filter(author=user)


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

    def form_valid(self, form):
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blog:post-list')


class CommentCreateView(View):

    @method_decorator(login_required)
    def post(self, request, pk):
        form = CommentForm(request.POST)
        if form.is_valid():
            post = Post.objects.get(pk=pk)
            form.instance.post = post
            form.instance.author = request.user
            form.save()
            if request.user != post.author:
                email_subject = 'New comment'
                author = post.author
                current_site = get_current_site(request)
                message = render_to_string('users/new_comment_email.html', {
                    'author': author.username,
                    'user': request.user.username,
                    'post': post,
                    'domain': current_site.domain,
                    'comment': form.cleaned_data.get('text'),
                })

                to_email = author.email
                send_mail_task.delay(email_subject, message, to_email)
                # email = EmailMessage(email_subject, message, to=[to_email])
                # email.send()
            return redirect('blog:post-detail', post.pk)