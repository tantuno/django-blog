from django.shortcuts import get_object_or_404,redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from .models import Post
from .forms import PostForm, CommentForm


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

    def post(self, request, **kwargs):
        if not request.user.is_authenticated:
            return redirect('blog:post-list')
        my_data = request.POST
        # print(request.META['HTTP_REFERER'].split('/'))
        post = Post.objects.get(pk=int(request.META['HTTP_REFERER'].split('/')[-2]))
        form = CommentForm(my_data)
        form.instance.post = post
        form.instance.author = request.user
        print(form)
        if form.is_valid():
            form.save()

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
        email = EmailMessage(email_subject, message, to=[to_email])
        email.send()
        return redirect('blog:post-detail', post.pk)

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

