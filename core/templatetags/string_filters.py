from django import template

register = template.Library()

@register.filter
def endswith_video(value):
    """Check if file URL ends with a video extension"""
    if not value:
        return False
    return value.lower().endswith(('.mp4', '.mov'))
