# Media Reviews

Personal tracker for keeping reviews on books, movies, anime, series, games and music. Each review includes title, media type, rating, author, release year and your thoughts.

## Functionality

- User registration and authentication
- Create, edit and delete reviews
- Filter by media type, author, title and minimum rating
- Paginated review list
- Import and export data in CSV, JSON, XLSX formats

## Import/Export Format

Each review contains the following fields:

| Field       | Type    | Constraints          | Description                            |
|-------------|---------|----------------------|----------------------------------------|
| `media_type`| string  | enum                 | Book, Movie, Anime, Series, Game, Music, Other |
| `title`     | string  | max 200 chars, unique| Name of the work                       |
| `rating`    | decimal | 1.0 - 10.0           | Your rating                            |
| `content`   | text    |                      | Your review                            |
| `author`    | string  | max 100 chars        | Author/Creator/Director/Artist         |
| `year`      | integer | 868 - 2030           | Year of release                        |

### JSON Example

```json
[
    {
        "media_type": "Movie",
        "title": "The Shawshank Redemption",
        "rating": "9.5",
        "content": "A masterpiece about hope and perseverance.",
        "author": "Frank Darabont",
        "year": 1994
    },
    {
        "media_type": "Book",
        "title": "1984",
        "rating": "9.0",
        "content": "A chilling dystopian novel.",
        "author": "George Orwell",
        "year": 1949
    }
]
```

## Stack

Django, PostgreSQL, HTMX, Tailwind CSS

## Run

1. `uv run python manage.py migrate`
2. `uv run python manage.py createsuperuser`
3. `./scripts/start_server.sh` or `uv run python manage.py tailwind runserver`