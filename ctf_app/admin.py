from django.contrib import admin
from .models import CTFUser, FlagSubmission, Challenge

@admin.register(CTFUser)
class CTFUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'session_key', 'is_authenticated', 'created_at', 'last_activity')
    list_filter = ('is_authenticated', 'created_at', 'last_activity')
    search_fields = ('username', 'session_key')
    readonly_fields = ('session_key', 'created_at')
    
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('-last_activity')

@admin.register(FlagSubmission)
class FlagSubmissionAdmin(admin.ModelAdmin):
    list_display = ('submitted_flag', 'is_correct', 'session_key', 'submitted_at', 'ip_address')
    list_filter = ('is_correct', 'submitted_at')
    search_fields = ('submitted_flag', 'session_key', 'ip_address')
    readonly_fields = ('submitted_at',)
    
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('-submitted_at')

@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('name', 'points', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at',)