from django.core.management.base import BaseCommand
from subscriptions.models import SubscriptionPlan

class Command(BaseCommand):
    help = 'Update the free plan to have a 30-day trial period.'

    def handle(self, *args, **options):
        try:
            # Get the existing free plan
            free_plan = SubscriptionPlan.objects.get(plan_type='free')
            
            # Update the plan
            free_plan.name = 'Free Trial'
            free_plan.duration_days = 30
            free_plan.save()
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully updated free plan: {free_plan.name} - {free_plan.duration_days} days'
                )
            )
            
        except SubscriptionPlan.DoesNotExist:
            self.stdout.write(
                self.style.ERROR('Free plan not found. Run seed_subscriptions first.')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error updating free plan: {e}')
            )

