from django.contrib import admin
from .models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'posted']
    list_filter = ['posted', 'author']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'posted', 'text']
    list_filter = ['posted', 'author', 'post']


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
