from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Subscription

class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
        ('Profile', {'fields': ('profile_picture', 'bio')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email', 'username')
    ordering = ('email',)

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('subscriber', 'target_user', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('subscriber__username', 'target_user__username')
    raw_id_fields = ('subscriber', 'target_user')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Subscription, SubscriptionAdmin)