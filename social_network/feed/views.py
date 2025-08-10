from django.core.paginator import Paginator
from django.shortcuts import render
from posts.models import Post
from accounts.models import Subscription
from django.contrib.auth.decorators import login_required


def home(request):
    posts_list = Post.objects.all().order_by('-created_at')
    paginator = Paginator(posts_list, 10)  # 10 постов на страницу
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    return render(request, 'feed/home.html', {
        'posts': posts,
        'feed_type': 'all'
    })


@login_required
def subscriptions_feed(request):
    try:
        subscribed_users_ids = Subscription.objects.filter(
            subscriber=request.user
        ).values_list('target_user_id', flat=True)

        # Добавляем посты текущего пользователя
        subscribed_users_ids = list(subscribed_users_ids) + [request.user.id]

        posts = Post.objects.filter(
            author_id__in=subscribed_users_ids
        ).select_related('author').order_by('-created_at')

        return render(request, 'feed/home.html', {
            'posts': posts,
            'feed_type': 'subscriptions'
        })
    except Exception as e:
        # Логирование ошибки для отладки
        print(f"Error in subscriptions_feed: {str(e)}")
        return redirect('feed:home')  # Перенаправляем на главную в случае ошибки