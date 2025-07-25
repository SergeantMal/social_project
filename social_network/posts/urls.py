from django.urls import path
from . import views

app_name = 'posts'  # Это определяет namespace 'feed'

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create_post, name='create'),
    path('<int:post_id>/edit/', views.edit_post, name='edit'),
    path('<int:post_id>/delete/', views.delete_post, name='delete'),
]