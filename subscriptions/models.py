from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import uuid


class SubscriptionPlan(models.Model):
    """Different subscription plans available"""
    
    PLAN_TYPES = [
        ('free', 'Free Plan'),
        ('monthly', 'Monthly Premium'),
        ('yearly', 'Yearly Premium'),
        ('lifetime', 'Lifetime Premium'),
    ]
    
    name = models.CharField(max_length=100)
    plan_type = models.CharField(max_length=20, choices=PLAN_TYPES, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.IntegerField(help_text="Duration in days (0 for lifetime)")
    features = models.JSONField(default=dict, help_text="Plan features as JSON")
    max_entries = models.IntegerField(default=-1, help_text="-1 for unlimited")
    max_reminders = models.IntegerField(default=-1, help_text="-1 for unlimited")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - ${self.price}/{self.get_duration_display()}"
    
    def get_duration_display(self):
        if self.duration_days == 0:
            return "Lifetime"
        elif self.duration_days <= 31:
            return "Month"
        elif self.duration_days <= 366:
            return "Year"
        else:
            return f"{self.duration_days} days"


class UserSubscription(models.Model):
    """User's current subscription status"""
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
        ('pending', 'Pending Payment'),
        ('trial', 'Trial Period'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='subscription')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    auto_renew = models.BooleanField(default=True)
    stripe_subscription_id = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.plan.name} ({self.status})"
    
    def is_active(self):
        """Check if subscription is currently active"""
        return (
            self.status in ['active', 'trial'] and 
            self.end_date > timezone.now()
        )
    
    def days_until_expiry(self):
        """Days remaining until subscription expires"""
        if self.end_date > timezone.now():
            return (self.end_date - timezone.now()).days
        return 0
    
    def needs_payment_reminder(self):
        """Check if user needs a payment reminder"""
        days_left = self.days_until_expiry()
        return days_left <= 7 and self.auto_renew and self.status == 'active'
    
    def extend_subscription(self):
        """Extend subscription for another period"""
        if self.plan.duration_days > 0:
            self.end_date = self.end_date + timedelta(days=self.plan.duration_days)
        self.status = 'active'
        self.save()


class PaymentHistory(models.Model):
    """Track all payment transactions"""
    
    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
        ('cancelled', 'Cancelled'),
    ]
    
    PAYMENT_METHODS = [
        ('stripe', 'Stripe'),
        ('paypal', 'PayPal'),
        ('bank', 'Bank Transfer'),
        ('manual', 'Manual'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subscription = models.ForeignKey(UserSubscription, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    stripe_payment_id = models.CharField(max_length=200, blank=True, null=True)
    transaction_id = models.CharField(max_length=200, blank=True, null=True)
    payment_date = models.DateTimeField(null=True, blank=True)
    failure_reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - ${self.amount} ({self.status})"


class PaymentReminder(models.Model):
    """Payment reminders for users"""
    
    REMINDER_TYPES = [
        ('renewal_7', '7 Days Before Renewal'),
        ('renewal_3', '3 Days Before Renewal'),
        ('renewal_1', '1 Day Before Renewal'),
        ('expired', 'Subscription Expired'),
        ('failed_payment', 'Failed Payment'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subscription = models.ForeignKey(UserSubscription, on_delete=models.CASCADE)
    reminder_type = models.CharField(max_length=20, choices=REMINDER_TYPES)
    scheduled_date = models.DateTimeField()
    sent_date = models.DateTimeField(null=True, blank=True)
    is_sent = models.BooleanField(default=False)
    email_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['scheduled_date']
        unique_together = ['user', 'subscription', 'reminder_type']
    
    def __str__(self):
        return f"{self.user.username} - {self.get_reminder_type_display()}"
    
    def mark_as_sent(self):
        """Mark reminder as sent"""
        self.is_sent = True
        self.sent_date = timezone.now()
        self.save()


class SubscriptionUsage(models.Model):
    """Track usage limits for subscription plans"""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='usage')
    entries_created = models.IntegerField(default=0)
    reminders_created = models.IntegerField(default=0)
    last_reset = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} Usage"
    
    def can_create_entry(self):
        """Check if user can create more entries"""
        subscription = getattr(self.user, 'subscription', None)
        if not subscription or subscription.plan.max_entries == -1:
            return True
        return self.entries_created < subscription.plan.max_entries
    
    def can_create_reminder(self):
        """Check if user can create more reminders"""
        subscription = getattr(self.user, 'subscription', None)
        if not subscription or subscription.plan.max_reminders == -1:
            return True
        return self.reminders_created < subscription.plan.max_reminders
    
    def reset_monthly_usage(self):
        """Reset usage counters (for monthly plans)"""
        self.entries_created = 0
        self.reminders_created = 0
        self.last_reset = timezone.now()
        self.save()
