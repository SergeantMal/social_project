from django.urls import path
from . import views
from .views import CustomLoginView

app_name = 'accounts'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # Более специфичные URL идут первыми
    path('profile/<str:username>/subscribe/', views.toggle_subscription, name='toggle_subscription'),
    path('profile/<str:username>/subscriptions/', views.subscriptions_list, name='subscriptions_list'),
    path('profile/<str:username>/subscribers/', views.subscribers_list, name='subscribers_list'),
    path('profile/<str:username>/', views.profile_view, name='user_profile'),

    # Общие URL идут после специфичных
    path('profile/', views.profile_view, name='profile'),  # Профиль текущего пользователя
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),
]