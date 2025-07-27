# messaging/context_processors.py
from .models import Message


def unread_messages_count(request):
    if request.user.is_authenticated:
        # Подсчитываем сообщения, где:
        # 1. Пользователь является участником беседы
        # 2. Сообщение не прочитано
        # 3. Сообщение отправлено не самим пользователем
        count = Message.objects.filter(
            conversation__participants=request.user,
            is_read=False
        ).exclude(sender=request.user).count()

        return {'unread_messages_count': count}
    return {}