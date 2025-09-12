from django.contrib import admin
from .models import Reminder


@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'time', 'category', 'priority', 'author', 'is_completed']
    list_filter = ['category', 'priority', 'is_completed', 'date']
    search_fields = ['title', 'description', 'location']
    date_hierarchy = 'date'
    readonly_fields = ['created_at', 'updated_at', 'completed_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'date', 'time')
        }),
        ('Classification', {
            'fields': ('category', 'priority', 'alert_preference')
        }),
        ('Details', {
            'fields': ('location', 'related_entry')
        }),
        ('Status', {
            'fields': ('is_completed', 'completed_at')
        }),
        ('Tracking', {
            'fields': ('author', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
