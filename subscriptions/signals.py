from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from .models import UserSubscription, SubscriptionPlan, PaymentReminder, SubscriptionUsage


@receiver(post_save, sender=User)
def create_user_subscription(sender, instance, created, **kwargs):
    """Create free subscription for new users"""
    if created:
        try:
            free_plan = SubscriptionPlan.objects.get(plan_type='free')
            UserSubscription.objects.create(
                user=instance,
                plan=free_plan,
                end_date=timezone.now() + timedelta(days=365*10),  # 10 years for free
                status='active'
            )
        except SubscriptionPlan.DoesNotExist:
            pass  # Free plan not yet created
        
        # Create usage tracking
        SubscriptionUsage.objects.create(user=instance)


@receiver(post_save, sender=UserSubscription)
def create_payment_reminders(sender, instance, created, **kwargs):
    """Create payment reminders when subscription is created/updated"""
    if instance.auto_renew and instance.status == 'active':
        # Delete existing reminders
        PaymentReminder.objects.filter(
            user=instance.user,
            subscription=instance
        ).delete()
        
        # Create new reminders
        reminders = [
            ('renewal_7', 7),
            ('renewal_3', 3),
            ('renewal_1', 1),
        ]
        
        for reminder_type, days_before in reminders:
            reminder_date = instance.end_date - timedelta(days=days_before)
            if reminder_date > timezone.now():
                PaymentReminder.objects.create(
                    user=instance.user,
                    subscription=instance,
                    reminder_type=reminder_type,
                    scheduled_date=reminder_date
                )


@receiver(pre_save, sender=UserSubscription)
def check_subscription_expiry(sender, instance, **kwargs):
    """Update subscription status based on expiry"""
    if instance.end_date <= timezone.now() and instance.status == 'active':
        instance.status = 'expired'
