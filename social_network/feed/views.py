from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.shortcuts import render
from posts.models import Post
from accounts.models import Subscription
from django.contrib.auth.decorators import login_required
from accounts.models import CustomUser


def search(request):
    query = request.GET.get('q', '').strip()
    results = {}

    if query:
        # Поиск по пользователям
        users = CustomUser.objects.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query)
        ).distinct()[:10]  # Ограничиваем результаты

        # Поиск по постам (текст и комментарии)
        posts = Post.objects.filter(
            Q(text__icontains=query) |
            Q(comments__text__icontains=query)
        ).distinct().order_by('-created_at')


        results = {
            'users': users,
            'posts': posts,
            'query': query
        }

    return render(request, 'feed/search_results.html', results)


def home(request):
    query = request.GET.get('q', '').strip()
    sort_by = request.GET.get('sort', 'newest')  # Получаем параметр сортировки

    posts_list = Post.objects.all()

    # Применяем сортировку
    if sort_by == 'oldest':
        posts_list = posts_list.order_by('created_at')  # Старые сверху
    elif sort_by == 'most_liked':
        posts_list = posts_list.annotate(likes_total=Count('likes')).order_by('-likes_total', '-created_at')
    elif sort_by == 'most_commented':
        posts_list = posts_list.annotate(comments_total=Count('comments')).order_by('-comments_total', '-created_at')
    else:  # newest (по умолчанию)
        posts_list = posts_list.order_by('-created_at')  # Новые сверху

    # Если есть поисковый запрос, фильтруем посты
    if query:
        posts_list = posts_list.filter(
            Q(text__icontains=query) |
            Q(author__username__icontains=query) |
            Q(comments__text__icontains=query)
        ).distinct()

    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    return render(request, 'feed/home.html', {
        'posts': posts,
        'feed_type': 'all',
        'search_query': query,
        'current_sort': sort_by  # Передаем текущий тип сортировки
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