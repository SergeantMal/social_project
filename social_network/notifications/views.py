from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Notification

@login_required
def all_notifications(request):
    notifications = Notification.objects.filter(user=request.user).select_related('sender').order_by('-created_at')
    return render(request, 'notifications/all.html', {'notifications': notifications})

@login_required
def mark_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    return JsonResponse({'status': 'success', 'redirect_url': notification.get_absolute_url()})

@login_required
def mark_all_as_read(request):
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return JsonResponse({'status': 'success'})