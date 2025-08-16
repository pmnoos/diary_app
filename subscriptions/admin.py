from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from .models import (
    SubscriptionPlan, UserSubscription, PaymentHistory, 
    PaymentReminder, SubscriptionUsage
)


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'plan_type', 'price', 'duration_display', 'max_entries', 'max_reminders', 'is_active']
    list_filter = ['plan_type', 'is_active']
    search_fields = ['name']
    ordering = ['price']
    
    def duration_display(self, obj):
        return obj.get_duration_display()
    duration_display.short_description = 'Duration'


@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'plan', 'status', 'start_date', 'end_date', 'days_remaining', 'auto_renew']
    list_filter = ['status', 'plan', 'auto_renew']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    def days_remaining(self, obj):
        days = obj.days_until_expiry()
        if days > 0:
            color = 'green' if days > 7 else 'orange' if days > 3 else 'red'
            return format_html(
                '<span style="color: {};">{} days</span>',
                color, days
            )
        return format_html('<span style="color: red;">Expired</span>')
    days_remaining.short_description = 'Days Left'
    
    actions = ['extend_subscription', 'mark_as_expired']
    
    def extend_subscription(self, request, queryset):
        for subscription in queryset:
            subscription.extend_subscription()
        self.message_user(request, f"Extended {queryset.count()} subscriptions")
    extend_subscription.short_description = "Extend selected subscriptions"
    
    def mark_as_expired(self, request, queryset):
        queryset.update(status='expired')
        self.message_user(request, f"Marked {queryset.count()} subscriptions as expired")
    mark_as_expired.short_description = "Mark as expired"


@admin.register(PaymentHistory)
class PaymentHistoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'amount', 'currency', 'status', 'payment_method', 'payment_date']
    list_filter = ['status', 'payment_method', 'currency']
    search_fields = ['user__username', 'user__email', 'transaction_id']
    readonly_fields = ['id', 'created_at']
    ordering = ['-created_at']
    
    def has_add_permission(self, request):
        return False  # Payments should only be created programmatically


@admin.register(PaymentReminder)
class PaymentReminderAdmin(admin.ModelAdmin):
    list_display = ['user', 'reminder_type', 'scheduled_date', 'is_sent', 'sent_date']
    list_filter = ['reminder_type', 'is_sent', 'email_sent']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'sent_date']
    ordering = ['scheduled_date']
    
    actions = ['mark_as_sent', 'reset_reminders']
    
    def mark_as_sent(self, request, queryset):
        for reminder in queryset:
            reminder.mark_as_sent()
        self.message_user(request, f"Marked {queryset.count()} reminders as sent")
    mark_as_sent.short_description = "Mark as sent"
    
    def reset_reminders(self, request, queryset):
        queryset.update(is_sent=False, sent_date=None, email_sent=False)
        self.message_user(request, f"Reset {queryset.count()} reminders")
    reset_reminders.short_description = "Reset selected reminders"


@admin.register(SubscriptionUsage)
class SubscriptionUsageAdmin(admin.ModelAdmin):
    list_display = ['user', 'entries_created', 'reminders_created', 'last_reset', 'can_create_more']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-updated_at']
    
    def can_create_more(self, obj):
        entries_ok = obj.can_create_entry()
        reminders_ok = obj.can_create_reminder()
        
        if entries_ok and reminders_ok:
            return format_html('<span style="color: green;">✓ All OK</span>')
        elif entries_ok:
            return format_html('<span style="color: orange;">⚠ Reminders limit reached</span>')
        elif reminders_ok:
            return format_html('<span style="color: orange;">⚠ Entries limit reached</span>')
        else:
            return format_html('<span style="color: red;">✗ All limits reached</span>')
    can_create_more.short_description = 'Usage Status'
    
    actions = ['reset_usage']
    
    def reset_usage(self, request, queryset):
        for usage in queryset:
            usage.reset_monthly_usage()
        self.message_user(request, f"Reset usage for {queryset.count()} users")
    reset_usage.short_description = "Reset monthly usage"


# Customize admin site
admin.site.site_header = "Diary App Administration"
admin.site.site_title = "Diary Admin"
admin.site.index_title = "Welcome to Diary App Administration"
