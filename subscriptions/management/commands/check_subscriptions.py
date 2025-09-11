from django.core.management.base import BaseCommand
from django.utils import timezone
from subscriptions.models import UserSubscription, PaymentReminder
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Check and update expired subscriptions'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--grace-period',
            type=int,
            default=3,
            help='Grace period in days after expiry before downgrading',
        )
    
    def handle(self, *args, **options):
        """Check for expired subscriptions and handle them"""
        grace_period = options['grace_period']
        grace_cutoff = timezone.now() - timezone.timedelta(days=grace_period)
        
        # Find expired subscriptions
        expired_subscriptions = UserSubscription.objects.filter(
            end_date__lt=timezone.now(),
            status='active'
        )
        
        # Find subscriptions past grace period
        grace_expired = UserSubscription.objects.filter(
            end_date__lt=grace_cutoff,
            status='expired'
        )
        
        # Update expired subscriptions
        updated_count = 0
        for subscription in expired_subscriptions:
            subscription.status = 'expired'
            subscription.save()
            updated_count += 1
            
            # Create expired notification
            PaymentReminder.objects.get_or_create(
                user=subscription.user,
                subscription=subscription,
                reminder_type='expired',
                defaults={
                    'scheduled_date': timezone.now(),
                }
            )
            
            self.stdout.write(
                f"Marked subscription as expired: {subscription.user.username}"
            )
        
        # Downgrade subscriptions past grace period
        downgraded_count = 0
        try:
            from subscriptions.models import SubscriptionPlan
            free_plan = SubscriptionPlan.objects.get(plan_type='free')
            
            for subscription in grace_expired:
                # Switch to free plan
                subscription.plan = free_plan
                subscription.status = 'active'
                subscription.end_date = timezone.now() + timezone.timedelta(days=365*10)
                subscription.auto_renew = False
                subscription.save()
                downgraded_count += 1
                
                self.stdout.write(
                    self.style.WARNING(
                        f"Downgraded to free plan: {subscription.user.username}"
                    )
                )
                
        except SubscriptionPlan.DoesNotExist:
            self.stdout.write(
                self.style.ERROR("Free plan not found - cannot downgrade users")
            )
        
        self.stdout.write(
            self.style.SUCCESS(
                f"Updated {updated_count} expired subscriptions, "
                f"downgraded {downgraded_count} to free plan"
            )
        )
