from django.contrib import admin
from .models import Conversation, Message


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'participants_list', 'created_at', 'updated_at')
    filter_horizontal = ('participants',)

    def participants_list(self, obj):
        return ", ".join([user.username for user in obj.participants.all()])


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'conversation', 'timestamp', 'is_read')
    list_filter = ('is_read', 'timestamp')
    search_fields = ('content', 'sender__username')