from django.shortcuts import render
from posts.models import Post
from accounts.models import Subscription


def home(request):
    if request.user.is_authenticated:
        # Получаем ID пользователей, на которых подписан текущий пользователь
        subscribed_users_ids = Subscription.objects.filter(
            subscriber=request.user
        ).values_list('target_user_id', flat=True)

        # Добавляем посты текущего пользователя
        subscribed_users_ids = list(subscribed_users_ids) + [request.user.id]

        posts = Post.objects.filter(
            author_id__in=subscribed_users_ids
        ).order_by('-created_at')
    else:
        posts = Post.objects.all().order_by('-created_at')

    return render(request, 'feed/home.html', {'posts': posts})