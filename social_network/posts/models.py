from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')  # Один пользователь - один лайк на пост

    def __str__(self):
        return f'{self.user} likes {self.post.id}'

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    text = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user}: {self.text[:20]}...'

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    text = models.TextField(max_length=1000)
    image = models.ImageField(upload_to='posts/images/', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, through=Like, related_name='liked_posts')
    comments = models.ManyToManyField(User, through=Comment, related_name='commented_posts')

    @property
    def likes_count(self):
        return self.likes.count()

    @property
    def comments_count(self):
        return self.comments.count()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Post by {self.author.username} at {self.created_at}'