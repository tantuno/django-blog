from django.contrib import admin
from .models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'posted']
    list_filter = ['posted', 'author']

admin.site.register(Post, PostAdmin)
