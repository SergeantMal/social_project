from django.db import models

# Create your models here.


from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def subscribe(self, user):
        """Подписаться на пользователя"""
        if self != user and not self.is_subscribed_to(user):
            Subscription.objects.create(subscriber=self, target_user=user)

    def unsubscribe(self, user):
        """Отписаться от пользователя"""
        Subscription.objects.filter(subscriber=self, target_user=user).delete()

    def is_subscribed_to(self, user):
        """Проверка подписки с явным запросом к БД"""
        return self.subscriptions.filter(target_user=user).exists()

    @property
    def subscribers_count(self):
        """Количество подписчиков"""
        return self.subscribers.count()

    @property
    def subscriptions_count(self):
        """Количество подписок"""
        return self.subscriptions.count()


class Subscription(models.Model):
    subscriber = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='subscriptions'
    )
    target_user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='subscribers'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('subscriber', 'target_user')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.subscriber} -> {self.target_user}'