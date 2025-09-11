from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from subscriptions.models import SubscriptionPlan, UserSubscription
from django.utils import timezone

class Command(BaseCommand):
    help = 'Assign a subscription plan to a specific user.'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, help='Username of the user to assign a subscription to')
        parser.add_argument('--plan', type=str, help='Plan type to assign (free, monthly, yearly, lifetime)')

    def handle(self, *args, **options):
        User = get_user_model()
        username = options['username']
        plan_type = options['plan']

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'User {username} does not exist.'))
            return

        try:
            plan = SubscriptionPlan.objects.get(plan_type=plan_type)
        except SubscriptionPlan.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Plan type {plan_type} does not exist.'))
            return

        # Set start and end dates
        start_date = timezone.now()
        if plan.duration_days == 0:
            end_date = None
        else:
            end_date = start_date + timezone.timedelta(days=plan.duration_days)

        subscription, created = UserSubscription.objects.get_or_create(
            user=user,
            defaults={
                'plan': plan,
                'start_date': start_date,
                'end_date': end_date,
                'status': 'active',
            }
        )
        if not created:
            subscription.plan = plan
            subscription.start_date = start_date
            subscription.end_date = end_date
            subscription.status = 'active'
            subscription.save()
            self.stdout.write(self.style.WARNING(f'Updated subscription for user {username} to plan {plan.name}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Assigned plan {plan.name} to user {username}'))
