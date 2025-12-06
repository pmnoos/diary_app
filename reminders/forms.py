from django import forms
from django.utils import timezone
from .models import Reminder


class ReminderForm(forms.ModelForm):
    class Meta:
        model = Reminder
        fields = ['title', 'description', 'date', 'time', 'category', 'priority', 
              'alert_preference', 'location', 'is_recurring', 'recurrence_type', 'is_completed']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter reminder title...',
                'maxlength': 200,
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Add details about this reminder...',
                'rows': 3,
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'min': timezone.now().date().isoformat(),  # Prevent past dates
            }),
            'time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time',
                'step': '300',  # 5-minute intervals
            }),
            'category': forms.Select(attrs={
                'class': 'form-control',
            }),
            'priority': forms.Select(attrs={
                'class': 'form-control',
            }),
            'alert_preference': forms.Select(attrs={
                'class': 'form-control',
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Optional: Add location...',
            }),
            'is_recurring': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            'recurrence_type': forms.Select(attrs={
                'class': 'form-control',
            }),
            'is_completed': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }
        help_texts = {
            'date': 'Select the date for your reminder',
            'time': 'Optional: Set a specific time',
            'category': 'Choose a category to organize your reminders',
            'priority': 'Set the importance level',
            'alert_preference': 'Choose how you want to be notified',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set default date to today if creating new reminder
        if not self.instance.pk:
            self.fields['date'].initial = timezone.now().date()
        
        # Make title field autofocus
        self.fields['title'].widget.attrs['autofocus'] = True
        
        # Add required field styling
        for field_name in ['title', 'date']:
            self.fields[field_name].widget.attrs['required'] = True


class QuickReminderForm(forms.ModelForm):
    """Simplified form for quick reminder creation"""
    class Meta:
        model = Reminder
        fields = ['title', 'date', 'time']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Quick reminder...',
                'autofocus': True,
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'value': timezone.now().date().isoformat(),
            }),
            'time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time',
                'step': '300',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].initial = timezone.now().date()
        self.fields['time'].required = False