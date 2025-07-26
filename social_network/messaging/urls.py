from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('', views.conversation_list, name='conversation_list'),
    path('new/<int:user_id>/', views.new_conversation, name='new_conversation'),
    path('<int:user_id>/', views.conversation_detail, name='conversation_detail'),
    path('api/can-message/<int:user_id>/', views.can_message_user, name='can_message'),
]