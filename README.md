# Media Reviews

Personal tracker for keeping reviews on books, movies, anime, series, games and music. Each review includes title, media type, rating, author, release year and your thoughts.

## Functionality

- User registration and authentication
- Create, edit and delete reviews
- Filter by media type, author, title and minimum rating
- Paginated review list
- Import and export data in CSV, JSON, XLSX formats

## Stack

Django, PostgreSQL, HTMX, Tailwind CSS

## Run

1. `uv run python manage.py migrate`
2. `uv run python manage.py createsuperuser`
3. `./scripts/start_server.sh` or `uv run python manage.py tailwind runserver`