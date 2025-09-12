from django.utils import timezone
from datetime import timedelta
from reminders.models import Reminder


def reminder_alerts(request):
    """
    Context processor to add reminder alerts to all templates
    """
    if not request.user.is_authenticated:
        return {}
    
    today = timezone.now().date()
    
    # Get different types of urgent reminders
    overdue_reminders = Reminder.objects.filter(
        author=request.user,
        is_completed=False,
        date__lt=today
    ).order_by('date')[:5]  # Limit to 5 most urgent
    
    today_reminders = Reminder.objects.filter(
        author=request.user,
        is_completed=False,
        date=today
    ).order_by('time')[:5]
    
    upcoming_reminders = Reminder.objects.filter(
        author=request.user,
        is_completed=False,
        date=today + timedelta(days=1)
    ).order_by('time')[:3]
    
    # High priority reminders (next 7 days)
    urgent_reminders = Reminder.objects.filter(
        author=request.user,
        is_completed=False,
        priority__in=['high', 'urgent'],
        date__range=[today, today + timedelta(days=7)]
    ).order_by('date', 'time')[:3]
    
    # Count totals for badges
    total_overdue = overdue_reminders.count()
    total_today = today_reminders.count()
    total_upcoming = Reminder.objects.filter(
        author=request.user,
        is_completed=False,
        date__gt=today
    ).count()
    total_urgent = Reminder.objects.filter(
        author=request.user,
        is_completed=False,
        date__lte=today + timedelta(days=3)
    ).count()
    
    return {
        'reminder_alerts': {
            'overdue': overdue_reminders,
            'today': today_reminders,
            'upcoming': upcoming_reminders,
            'urgent': urgent_reminders,
            'counts': {
                'overdue': total_overdue,
                'today': total_today,
                'upcoming': total_upcoming,
                'urgent': total_urgent,
                'total_pending': Reminder.objects.filter(
                    author=request.user, 
                    is_completed=False
                ).count()
            }
        }
    }
