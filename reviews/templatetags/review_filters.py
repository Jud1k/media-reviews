from django import template

register = template.Library()


@register.filter
def rating_color(rating: float) -> str:
    if rating >= 8:
        return "text-green-600"
    elif rating >= 6:
        return "text-yellow-600"
    else:
        return "text-red-600"