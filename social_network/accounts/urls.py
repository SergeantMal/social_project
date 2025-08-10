from django.urls import path, reverse_lazy
from . import views
from .forms import CustomPasswordResetForm
from .views import CustomLoginView, InstantPasswordResetView
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('users/', views.user_list, name='user_list'),

    # Сначала специфичные URL для редактирования профиля
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),

    # Затем URL с динамическими параметрами
    path('profile/<str:username>/subscribe/', views.toggle_subscription, name='toggle_subscription'),
    path('profile/<str:username>/subscriptions/', views.subscriptions_list, name='subscriptions_list'),
    path('profile/<str:username>/subscribers/', views.subscribers_list, name='subscribers_list'),

    # Общий URL для профиля текущего пользователя
    path('profile/', views.profile_view, name='profile'),

    # URL для профиля конкретного пользователя (должен быть последним в этой группе)
    path('profile/<str:username>/', views.profile_view, name='user_profile'),

    # URL для сброса пароля
    path('password_reset/',
         auth_views.PasswordResetView.as_view(
             template_name='accounts/registration/password_reset_form.html',
             email_template_name='accounts/registration/password_reset_email.html',
             subject_template_name='accounts/registration/password_reset_subject.txt',
             success_url=reverse_lazy('accounts:password_reset_done')
         ),
         name='password_reset'),

    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='accounts/registration/password_reset_done.html'
         ),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='accounts/registration/password_reset_confirm.html',
             success_url=reverse_lazy('accounts:password_reset_complete')
         ),
         name='password_reset_confirm'),  # Это имя должно совпадать с шаблоном письма

    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='accounts/registration/password_reset_complete.html'
         ),
         name='password_reset_complete'),

    # Ваш instant сброс пароля
    path('password_reset_instant/',
         InstantPasswordResetView.as_view(),
         name='password_reset_instant'),
    ]