from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('', views.all_notifications, name='all'),
    path('read/<int:notification_id>/', views.mark_as_read, name='mark_as_read'),
    path('read-all/', views.mark_all_as_read, name='mark_all_as_read'),
]