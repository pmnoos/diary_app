from django import forms
from django.utils import timezone
from .models import Entry

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['title', 'date', 'content', 'image', 'is_private']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter a title for your entry...'
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'max': timezone.now().strftime('%Y-%m-%d')  # Can't pick future dates
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control rich-text',
                'placeholder': 'Write your thoughts here... You can include links by typing: https://example.com',
                'rows': 12
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'is_private': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
        labels = {
            'title': 'Entry Title',
            'date': 'Entry Date',
            'content': 'Your Thoughts',
            'image': 'Add an Image (optional)',
            'is_private': 'Keep this entry private'
        }
        help_texts = {
            'title': 'Give your diary entry a meaningful title',
            'date': 'Choose the date this entry is for (you can backdate entries for missed days)',
            'content': 'You can include links in your text - just type the full URL (e.g., https://example.com)',
            'image': 'Upload a photo to accompany your diary entry (JPG, PNG, GIF)',
            'is_private': 'Check this box to keep your entry private (recommended for personal thoughts)'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set default date to today if creating a new entry
        if not self.instance.pk:
            self.fields['date'].initial = timezone.now().date()
        
        # Update max date to today (can't pick future dates)
        self.fields['date'].widget.attrs['max'] = timezone.now().strftime('%Y-%m-%d')
