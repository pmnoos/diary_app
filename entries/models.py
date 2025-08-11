from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
import os

def user_directory_path(instance, filename):
    """File will be uploaded to MEDIA_ROOT/diary_images/user_<id>/<filename>"""
    return f'diary_images/user_{instance.author.id}/{filename}'

class Entry(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date = models.DateField(default=timezone.now, help_text="The date this diary entry is for")
    image = models.ImageField(upload_to=user_directory_path, blank=True, null=True, 
                             help_text="Optional: Upload an image for your diary entry")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='diary_entries')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_private = models.BooleanField(default=True)  # For future feature to share entries
    
    class Meta:
        ordering = ['-date', '-created_at']  # Show entries by diary date, then creation time
        verbose_name_plural = "entries"
    
    def __str__(self):
        return f"{self.title} by {self.author.username}"
    
    def get_absolute_url(self):
        return reverse('entry_detail', kwargs={'pk': self.pk})
    
    def get_snippet(self, length=100):
        """Return a truncated version of the content for previews"""
        if len(self.content) <= length:
            return self.content
        return self.content[:length] + "..."
