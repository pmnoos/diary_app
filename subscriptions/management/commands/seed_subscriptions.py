from django.core.management.base import BaseCommand
from subscriptions.models import SubscriptionPlan

class Command(BaseCommand):
    help = 'Seed the database with demo subscription plans.'

    def handle(self, *args, **options):
        plans = [
            {
                'name': 'Free',
                'plan_type': 'free',
                'price': 0.00,
                'duration_days': 0,
                'features': {
                    'entries_per_month': 30,
                    'reminders': 5,
                    'support': 'Community',
                },
                'is_active': True,
            },
            {
                'name': 'Pro Monthly',
                'plan_type': 'monthly',
                'price': 4.99,
                'duration_days': 30,
                'features': {
                    'entries_per_month': 'Unlimited',
                    'reminders': 50,
                    'support': 'Priority',
                },
                'is_active': True,
            },
            {
                'name': 'Pro Yearly',
                'plan_type': 'yearly',
                'price': 49.99,
                'duration_days': 365,
                'features': {
                    'entries_per_month': 'Unlimited',
                    'reminders': 100,
                    'support': 'Priority',
                },
                'is_active': True,
            },
        ]

        for plan_data in plans:
            plan, created = SubscriptionPlan.objects.get_or_create(
                name=plan_data['name'],
                defaults=plan_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created plan: {plan.name}"))
            else:
                self.stdout.write(self.style.WARNING(f"Plan already exists: {plan.name}"))

        self.stdout.write(self.style.SUCCESS('Subscription plans seeded.'))
