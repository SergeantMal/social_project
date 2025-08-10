from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post
from .forms import PostCreateForm, PostEditForm, CommentForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Like, Comment
from notifications.models import Notification
import json

def home(request):
    return render(request, 'posts/home.html')


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostCreateForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            # Создаем уведомления для подписчиков
            subscribers = request.user.subscribers.all()
            for subscription in subscribers:
                Notification.objects.create(
                    user=subscription.subscriber,  # Используем subscriber из подписки
                    sender=request.user,
                    notification_type='post',
                    object_id=post.id
                )

            messages.success(request, 'Пост успешно опубликован!')
            return redirect('feed:home')
    else:
        form = PostCreateForm()
    return render(request, 'posts/create_post.html', {'form': form})

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)

    if request.method == 'POST':
        form = PostEditForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Пост успешно отредактирован!')
            return redirect('feed:home')
    else:
        form = PostEditForm(instance=post)
    return render(request, 'posts/edit_post.html', {'form': form, 'post': post})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == 'POST':
        post.delete()
    return JsonResponse({'success': True})


@require_POST
@login_required
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    liked = False

    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
        liked = True
        # Создаем уведомление
        if request.user != post.author:
            Notification.objects.create(
                user=post.author,
                sender=request.user,
                notification_type='like',
                object_id=post.id
            )

    return JsonResponse({
        'liked': liked,
        'likes_count': post.likes.count()
    })


@require_POST
@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    try:
        data = json.loads(request.body)
        print("Received data:", data)  # Что приходит на сервер?

        form = CommentForm(data)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            print("Comment saved:", comment.id, comment.text)  # Проверка сохранения

            # Создаем уведомление
            if request.user != post.author:
                Notification.objects.create(
                    user=post.author,
                    sender=request.user,
                    notification_type='comment',
                    object_id=post.id
                )

            return JsonResponse({
                'success': True,
                'comment': {
                    'id': comment.id,
                    'text': comment.text,
                    'user': comment.user.username,
                    'created_at': comment.created_at.strftime('%b %d, %Y %H:%M')
                },
                'comments_count': post.comments.count()
            })
        else:
            print("Form errors:", form.errors)
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)

    except Exception as e:
        print("Error:", str(e))
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@require_POST
@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    post = comment.post
    comment.delete()

    return JsonResponse({
        'success': True,
        'comments_count': post.comments_count
    })



def post_detail(request, pk):
    # Для детальной страницы поста
    post = get_object_or_404(Post.objects.prefetch_related('comments__user', 'likes'), pk=pk)
    return render(request, 'posts/post_detail.html', {'post': post})