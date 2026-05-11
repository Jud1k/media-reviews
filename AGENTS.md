# AGENTS.md

## Running the App

- Start dev server: `uv run python manage.py tailwind runserver` (not plain `runserver` - Tailwind CSS won't work)
- Or use: `./scripts/start_server.sh`

## Database

- PostgreSQL required
- Defaults: `media_reviews` / `postgres` / `postgres` @ localhost:5432

## Django Commands

- Migration: `uv run python manage.py migrate`
- Create superuser: `uv run python manage.py createsuperuser`

## Lint & Type Check

- Lint: `uv run ruff check .`
- Type check: `uv run mypy .`

## Tech Stack

- Django 6.0 + Python 3.13+
- HTMX + Tailwind CLI
- PostgreSQL

## Apps

- `reviews` - main media review functionality
- `registration` - authentication (built-in Django auth)