from django.db import models
from django.conf import settings
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=120)
    content = models.TextField()
    posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name='posts')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post-detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-posted']
        verbose_name_plural = 'Posts'


class Comment(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE)
    text = models.TextField()
    posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['-posted']
        verbose_name_plural = 'Comments'
