from django.urls import path
from . import views

app_name = 'feed'  # Это определяет namespace 'feed'

urlpatterns = [
    path('', views.home, name='home'),
]