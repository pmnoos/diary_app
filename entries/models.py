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
    
    # New archiving and organization fields
    is_archived = models.BooleanField(default=False, help_text="Archive old entries to improve performance")
    archived_at = models.DateTimeField(blank=True, null=True, help_text="When this entry was archived")
    tags = models.CharField(max_length=500, blank=True, help_text="Comma-separated tags for easy searching (e.g., travel, work, family)")
    mood = models.CharField(max_length=50, blank=True, 
                           choices=[
                               ('happy', '😊 Happy'),
                               ('sad', '😢 Sad'),
                               ('excited', '🎉 Excited'),
                               ('calm', '😌 Calm'),
                               ('stressed', '😰 Stressed'),
                               ('grateful', '🙏 Grateful'),
                               ('reflective', '🤔 Reflective'),
                               ('energetic', '⚡ Energetic'),
                               ('peaceful', '☮️ Peaceful'),
                               ('other', '📝 Other'),
                           ], help_text="How were you feeling during this entry?")
    
    # Performance fields
    word_count = models.IntegerField(default=0, help_text="Automatically calculated word count")
    
    class Meta:
        ordering = ['-date', '-created_at']  # Show entries by diary date, then creation time
        verbose_name_plural = "entries"
        indexes = [
            models.Index(fields=['author', 'is_archived', 'date']),  # Performance index
            models.Index(fields=['author', 'mood']),  # Mood filtering
            models.Index(fields=['created_at']),  # Chronological queries
        ]
    
    def __str__(self):
        return f"{self.title} by {self.author.username}"
    
    def get_absolute_url(self):
        return reverse('entry_detail', kwargs={'pk': self.pk})
    
    def get_snippet(self, length=100):
        """Return a truncated version of the content for previews"""
        if len(self.content) <= length:
            return self.content
        return self.content[:length] + "..."
    
    def save(self, *args, **kwargs):
        """Override save to calculate word count and handle archiving"""
        # Calculate word count
        self.word_count = len(self.content.split()) if self.content else 0
        
        # Set archived_at timestamp when archiving
        if self.is_archived and not self.archived_at:
            self.archived_at = timezone.now()
        elif not self.is_archived:
            self.archived_at = None
            
        super().save(*args, **kwargs)
    
    def archive(self):
        """Archive this entry"""
        self.is_archived = True
        self.archived_at = timezone.now()
        self.save()
    
    def unarchive(self):
        """Unarchive this entry"""
        self.is_archived = False
        self.archived_at = None
        self.save()
    
    @property
    def age_in_days(self):
        """Calculate how old this entry is"""
        return (timezone.now().date() - self.date).days
    
    @property
    def can_auto_archive(self):
        """Check if entry is old enough for auto-archiving (older than 6 months)"""
        return self.age_in_days > 180 and not self.is_archived
    
    def get_tag_list(self):
        """Return tags as a list"""
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
    
    def get_snippet(self, length=100):
        """Return a truncated version of the content for previews"""
        if len(self.content) <= length:
            return self.content
        return self.content[:length] + "..."
