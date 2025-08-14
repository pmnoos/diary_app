from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


class Reminder(models.Model):
    CATEGORY_CHOICES = [
        ('personal', '👤 Personal'),
        ('work', '💼 Work'),
        ('health', '🏥 Health'), 
        ('social', '👥 Social'),
        ('birthday', '🎂 Birthday'),
        ('appointment', '📅 Appointment'),
        ('deadline', '⏰ Deadline'),
        ('event', '🎉 Event'),
        ('travel', '✈️ Travel'),
        ('other', '📝 Other'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', '🟢 Low'),
        ('medium', '🟡 Medium'), 
        ('high', '🔴 High'),
        ('urgent', '🆘 Urgent'),
    ]
    
    ALERT_CHOICES = [
        ('none', 'No alerts'),
        ('day_of', 'Day of event'),
        ('1_day', '1 day before'),
        ('3_days', '3 days before'),
        ('1_week', '1 week before'),
        ('custom', 'Custom alerts'),
    ]
    
    title = models.CharField(max_length=200, help_text="What do you need to remember?")
    description = models.TextField(blank=True, help_text="Additional details about this reminder")
    date = models.DateField(help_text="When is this event/deadline?")
    time = models.TimeField(blank=True, null=True, help_text="What time? (optional)")
    
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='personal')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    alert_preference = models.CharField(max_length=10, choices=ALERT_CHOICES, default='1_day')
    
    location = models.CharField(max_length=200, blank=True, help_text="Where is this happening? (optional)")
    
    # Tracking
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reminders')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Status
    is_completed = models.BooleanField(default=False, help_text="Mark as done")
    completed_at = models.DateTimeField(blank=True, null=True)
    
    # Optional link to diary entry when event happens
    related_entry = models.ForeignKey('entries.Entry', on_delete=models.SET_NULL, 
                                    blank=True, null=True, 
                                    help_text="Link to diary entry about this event")
    
    class Meta:
        ordering = ['date', 'time', '-priority']
        verbose_name_plural = "reminders"
    
    def __str__(self):
        return f"{self.title} ({self.date})"
    
    def get_absolute_url(self):
        return reverse('reminder_detail', kwargs={'pk': self.pk})
    
    @property
    def days_until(self):
        """Calculate days until the reminder date"""
        today = timezone.now().date()
        delta = self.date - today
        return delta.days
    
    @property
    def is_overdue(self):
        """Check if reminder date has passed and not completed"""
        return self.date < timezone.now().date() and not self.is_completed
    
    @property
    def is_today(self):
        """Check if reminder is for today"""
        return self.date == timezone.now().date()
    
    @property
    def is_this_week(self):
        """Check if reminder is within next 7 days"""
        return 0 <= self.days_until <= 7
    
    @property
    def urgency_level(self):
        """Get urgency based on days until and priority"""
        days = self.days_until
        if self.is_overdue:
            return 'overdue'
        elif days == 0:
            return 'today'
        elif days <= 1:
            return 'tomorrow'
        elif days <= 3:
            return 'soon'
        elif days <= 7:
            return 'this_week'
        else:
            return 'future'
    
    def mark_completed(self):
        """Mark reminder as completed"""
        self.is_completed = True
        self.completed_at = timezone.now()
        self.save()
