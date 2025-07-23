from django.urls import path
from . import views

app_name = 'posts'  # Это определяет namespace 'feed'

urlpatterns = [
    path('', views.home, name='home'),
]