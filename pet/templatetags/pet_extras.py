from django import template

register = template.Library()

@register.filter
def safe_url(image_field):
    """
    Safely retrieves the URL of an image field.
    Returns empty string if the field has no file or raises ValueError.
    """
    if image_field:
        try:
            return image_field.url
        except ValueError:
            # Catch "The 'image' attribute has no file associated with it."
            return ""
        except Exception:
            return ""
    return ""
