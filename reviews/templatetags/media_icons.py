from django import template

register = template.Library()


MEDIA_TYPE_ICONS = {
    "Book": "icon-book",
    "Movie": "icon-movie",
    "Game": "icon-game",
    "Anime": "icon-anime",
    "Series": "icon-series",
    "Music": "icon-music",
}


@register.simple_tag
def get_media_icon(media_type: str) -> str:
    return MEDIA_TYPE_ICONS.get(media_type, "icon-default")