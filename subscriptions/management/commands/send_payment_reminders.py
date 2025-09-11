from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from subscriptions.models import PaymentReminder
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Send payment reminders to users'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be sent without actually sending emails',
        )
    
    def handle(self, *args, **options):
        """Send payment reminders"""
        dry_run = options['dry_run']
        
        # Get reminders that need to be sent
        pending_reminders = PaymentReminder.objects.filter(
            scheduled_date__lte=timezone.now(),
            is_sent=False
        ).select_related('user', 'subscription', 'subscription__plan')
        
        sent_count = 0
        
        for reminder in pending_reminders:
            try:
                if dry_run:
                    self.stdout.write(
                        f"Would send {reminder.get_reminder_type_display()} "
                        f"to {reminder.user.email}"
                    )
                else:
                    success = self.send_reminder_email(reminder)
                    if success:
                        reminder.mark_as_sent()
                        reminder.email_sent = True
                        reminder.save()
                        sent_count += 1
                        
                        self.stdout.write(
                            self.style.SUCCESS(
                                f"Sent {reminder.get_reminder_type_display()} "
                                f"to {reminder.user.email}"
                            )
                        )
                    else:
                        self.stdout.write(
                            self.style.ERROR(
                                f"Failed to send reminder to {reminder.user.email}"
                            )
                        )
                        
            except Exception as e:
                logger.error(f"Error sending reminder {reminder.id}: {e}")
                self.stdout.write(
                    self.style.ERROR(f"Error sending reminder: {e}")
                )
        
        if not dry_run:
            self.stdout.write(
                self.style.SUCCESS(f"Sent {sent_count} payment reminders")
            )
    
    def send_reminder_email(self, reminder):
        """Send email reminder to user"""
        try:
            user = reminder.user
            subscription = reminder.subscription
            
            # Email subject based on reminder type
            subject_map = {
                'renewal_7': 'Your Diary subscription expires in 7 days',
                'renewal_3': 'Your Diary subscription expires in 3 days',
                'renewal_1': 'Your Diary subscription expires tomorrow',
                'expired': 'Your Diary subscription has expired',
                'failed_payment': 'Payment failed for your Diary subscription',
            }
            
            subject = subject_map.get(
                reminder.reminder_type, 
                'Diary subscription update'
            )
            
            # Prepare email context
            context = {
                'user': user,
                'subscription': subscription,
                'reminder_type': reminder.reminder_type,
                'days_left': subscription.days_until_expiry(),
                'renewal_url': f"{settings.SITE_URL}/subscriptions/renew/",
                'manage_url': f"{settings.SITE_URL}/subscriptions/manage/",
            }
            
            # Render email templates
            html_message = render_to_string(
                'subscriptions/emails/payment_reminder.html', 
                context
            )
            plain_message = render_to_string(
                'subscriptions/emails/payment_reminder.txt', 
                context
            )
            
            # Send email
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                html_message=html_message,
                fail_silently=False,
            )
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email to {user.email}: {e}")
            return False
