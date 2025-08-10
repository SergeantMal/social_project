from django.urls import path
from . import views

app_name = 'feed'  # Это определяет namespace 'feed'


urlpatterns = [
    path('', views.home, name='home'),
    path('subscriptions/', views.subscriptions_feed, name='subscriptions'),
]
