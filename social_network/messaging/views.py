from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import Conversation, Message
from .forms import MessageForm

User = get_user_model()


@login_required
def conversation_list(request):
    conversations = Conversation.objects.filter(
        participants=request.user
    ).prefetch_related('participants', 'messages').order_by('-updated_at')

    return render(request, 'messaging/conversation_list.html', {
        'conversations': conversations,
        'current_user': request.user  # Передаем явно
    })

@login_required
def conversation_detail(request, user_id):
    other_user = get_object_or_404(User, id=user_id)

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

    messages = conversation.messages.all().order_by('timestamp')

    return render(request, 'messaging/conversation_detail.html', {
        'conversation': conversation,
        'other_user': other_user,
        'messages': messages,
        'form': form
    })


@login_required
def new_conversation(request, user_id):
    return conversation_detail(request, user_id)