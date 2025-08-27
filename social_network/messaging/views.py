from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from accounts.models import CustomUser
from .models import Conversation
from .forms import MessageForm
from django.core.exceptions import PermissionDenied

User = get_user_model()


@login_required
def conversation_list(request):
    conversations = Conversation.objects.filter(
        participants=request.user
    ).prefetch_related('participants', 'messages').order_by('-updated_at')

    return render(request, 'messaging/conversation_list.html', {
        'conversations': conversations,
        'request': request  # Важно передать request
    })

@login_required
def conversation_detail(request, user_id):
    other_user = get_object_or_404(CustomUser, id=user_id)

    # Проверка, что пользователь не пытается писать сам себе
    if request.user == other_user:
        return redirect('messaging:conversation_list')

    # Найдем или создадим диалог
    conversation = Conversation.objects.filter(
        participants=request.user
    ).filter(
        participants=other_user
    ).first()

    if not conversation:
        conversation = Conversation.objects.create()
        conversation.participants.add(request.user, other_user)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.conversation = conversation
            message.sender = request.user
            message.save()
            conversation.save()  # Обновляем updated_at
            return redirect('messaging:conversation_detail', user_id=user_id)
    else:
        form = MessageForm()

    # Помечаем сообщения как прочитанные
    conversation.messages.filter(is_read=False).exclude(sender=request.user).update(is_read=True)

    messages = conversation.messages.all().select_related('sender').order_by('timestamp')

    return render(request, 'messaging/conversation_detail.html', {
        'conversation': conversation,
        'other_user': other_user,
        'chat_messages': messages,
        'form': form
    })


def check_message_permission(view_func):
    """Декоратор для проверки прав на отправку сообщения"""
    def wrapper(request, user_id, *args, **kwargs):
        other_user = get_object_or_404(User, id=user_id)
        if not other_user.can_receive_message_from(request.user):
            raise PermissionDenied("You can't send messages to this user")
        return view_func(request, user_id, *args, **kwargs)
    return wrapper

@login_required
@check_message_permission
def new_conversation(request, user_id):
    other_user = get_object_or_404(CustomUser, id=user_id)

    if not other_user.can_receive_message_from(request.user):
        return redirect('accounts:user_profile', username=other_user.username)

    # Проверяем, есть ли уже диалог
    conversation = Conversation.objects.filter(
        participants=request.user
    ).filter(
        participants=other_user
    ).first()

    if not conversation:
        conversation = Conversation.objects.create()
        conversation.participants.add(request.user, other_user)

    return redirect('messaging:conversation_detail', user_id=user_id)

@login_required
def can_message_user(request, user_id):
    other_user = get_object_or_404(CustomUser, id=user_id)
    can_message = other_user.can_receive_message_from(request.user)
    return JsonResponse({
        'can_message': can_message,
        'message': "You can't message this user" if not can_message else ""
    })