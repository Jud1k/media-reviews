import csv
import io
from decimal import Decimal
from typing import Any, Generator
from openpyxl import Workbook, load_workbook
import json

from loguru import logger

from reviews.models import Review

REVIEWS_HEADERS = ["media_type", "title", "rating", "content", "author", "year"]


def create_reviews_from_csv(file_content, user) -> tuple[int, list[str]]:
    lines = file_content.splitlines()
    delimiter = "," if lines[0].count(",") > 1 else ";"
    reader = csv.DictReader(lines, delimiter=delimiter)
    count, errors = _create_reviews(reader, user)
    return count, errors


def create_reviews_from_json(file_content, user) -> tuple[int, list[str]]:
    try:
        reviews = json.loads(file_content)
    except json.JSONDecodeError as e:
        logger.error(f"Error while decoding JSON: {e}")
        return 0, ["JSON decoding error: {e}"]
    count, errors = _create_reviews(reviews, user)
    return count, errors


def create_reviews_from_xlsx(file_content, user) -> tuple[int, list[str]]:
    wb = load_workbook(file_content)
    sheet = wb.active
    headers = [cell.value for cell in sheet[1]]
    rows = []
    for row in sheet.iter_rows(min_row=2, max_col=7):
        row_dict = {headers[i]: row[i].value for i in range(len(headers))}
        rows.append(row_dict)
    count, errors = _create_reviews(rows, user)
    return count, errors


def _create_reviews(reviews, user):
    count = 0
    errors = []
    for review in reviews:
        try:
            new_review = Review(
                user=user,
                title=review["title"],
                rating=Decimal(review["rating"]),
                content=review["content"],
                media_type=review["media_type"],
                author=review["author"],
                year=int(review["year"]),
            )
            new_review.full_clean()
            new_review.save()
            count += 1
        except Exception as e:
            logger.error(f"Error while importing review: {e}")
            if isinstance(review, dict):
                errors.append(f"Row '{review.get('title', 'Unknown')}': {e}")
            else:
                errors.append(f"Row {review}: {e}")
    return count, errors


def get_reviews_csv(reviews: list[Review]) -> Generator[str, None, None]:
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, REVIEWS_HEADERS)
    writer.writeheader()
    yield buffer.getvalue()
    buffer.truncate(0)
    buffer.seek(0)
    for review in reviews:
        writer.writerow(
            {
                "media_type": review.media_type,
                "title": review.title,
                "rating": review.rating,
                "content": review.content,
                "author": review.author,
                "year": review.year,
            }
        )
        yield buffer.getvalue()
        buffer.truncate(0)
        buffer.seek(0)


def get_reviews_json(reviews: list[Review]) -> dict[str, Any]:
    json_data = []
    for review in reviews:
        json_data.append(
            {
                "media_type": review.media_type,
                "title": review.title,
                "rating": str(review.rating),
                "content": review.content,
                "author": review.author,
                "year": review.year,
            }
        )
    return json.dumps(json_data)


def get_reviews_xlsx(reviews: list[Review]) -> bytes:
    wb = Workbook()
    sheet = wb.active
    sheet.append(REVIEWS_HEADERS)
    for review in reviews:
        sheet.append(
            [
                review.media_type,
                review.title,
                review.rating,
                review.content,
                review.author,
                review.year,
            ]
        )
    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    return buffer
