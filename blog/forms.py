from django.forms import ModelForm
from .models import Post, Comment


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
