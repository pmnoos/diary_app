import re
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def urlize_target_blank(text):
    """
    Convert URLs in text to clickable links that open in a new tab.
    Also preserves line breaks.
    """
    # First, escape HTML characters for safety
    from django.utils.html import escape, linebreaks
    
    # Escape the text first
    text = escape(text)
    
    # Convert line breaks to <br> tags
    text = linebreaks(text)
    
    # URL pattern to match http, https, www links
    url_pattern = re.compile(
        r'(https?://[^\s<>"]+|www\.[^\s<>"]+)',
        re.IGNORECASE
    )
    
    def replace_url(match):
        url = match.group(0)
        # Add https:// if it starts with www
        if url.startswith('www.'):
            href = 'https://' + url
        else:
            href = url
        return f'<a href="{href}" target="_blank" rel="noopener noreferrer" style="color: #007bff; text-decoration: underline;">{url}</a>'
    
    # Replace URLs with clickable links
    text = url_pattern.sub(replace_url, text)
    
    return mark_safe(text)
