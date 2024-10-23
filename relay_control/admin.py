from django.contrib import admin
from .models import UnlockEvent

@admin.register(UnlockEvent)
class UnlockEventAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'status', 'ip_address')
    list_filter = ('status', 'created_at')
    search_fields = ('ip_address', 'error_message')
    readonly_fields = ('created_at',)