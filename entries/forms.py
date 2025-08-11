from django import forms
from django.utils import timezone
from .models import Entry

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['title', 'content', 'image', 'is_private']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': f'Enter a title for your entry... (Today: {timezone.now().strftime("%A, %B %d, %Y")})'
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
            'content': 'Your Thoughts',
            'image': 'Add an Image (optional)',
            'is_private': 'Keep this entry private'
        }
        help_texts = {
            'title': f'Writing on {timezone.now().strftime("%A, %B %d, %Y")}',
            'content': 'You can include links in your text - just type the full URL (e.g., https://example.com)',
            'image': 'Upload a photo to accompany your diary entry (JPG, PNG, GIF)',
            'is_private': 'Check this box to keep your entry private (recommended for personal thoughts)'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Update the title placeholder with current date each time the form is instantiated
        current_date = timezone.now().strftime("%A, %B %d, %Y")
        self.fields['title'].widget.attrs['placeholder'] = f'Enter a title for your entry... (Today: {current_date})'
        self.fields['title'].help_text = f'Writing on {current_date}'
