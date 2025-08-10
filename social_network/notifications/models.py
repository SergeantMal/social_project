# notifications/models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('like', 'Лайк'),
        ('comment', 'Комментарий'),
        ('post', 'Новый пост'),
        ('follow', 'Подписка'),
        ('message', 'Сообщение'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    object_id = models.PositiveIntegerField(null=True, blank=True)  # ID связанного объекта
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=255)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.sender} -> {self.user}: {self.notification_type}"

    def get_absolute_url(self):
        if self.notification_type == 'post':
            return reverse('posts:detail', kwargs={'pk': self.object_id})
        elif self.notification_type == 'like':
            return reverse('posts:detail', kwargs={'pk': self.object_id})
        elif self.notification_type == 'comment':
            return reverse('posts:detail', kwargs={'pk': self.object_id}) + f'#comment-{self.object_id}'
        elif self.notification_type == 'follow':  # Изменили с 'subscription' на 'follow'
            return reverse('accounts:user_profile', kwargs={'username': self.sender.username})
        elif self.notification_type == 'message':
            return reverse('messages:thread', kwargs={'thread_id': self.object_id})
        return reverse('notifications:all')