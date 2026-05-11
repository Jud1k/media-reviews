import io

from django.test import TestCase
from django.contrib.auth.models import User

from reviews.models import Review, MediaType
from reviews.service import export_reviews_csv, create_reviews_from_csv, CSV_HEADERS


class ExportReviewsCsvTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="pass"
        )
        self.review = Review.objects.create(
            user=self.user,
            title="Test Movie",
            media_type=MediaType.MOVIE,
            rating=8.5,
            content="Great movie!",
            author="Director",
            year=2024,
        )

    def test_export_returns_csv_with_header(self):
        response = export_reviews_csv(Review.objects.all())
        content = response.content.decode("utf-8")
        self.assertIn("media_type", content)
        self.assertIn("title", content)
        self.assertIn("rating", content)
        self.assertIn("content", content)
        self.assertIn("author", content)
        self.assertIn("year", content)

    def test_export_contains_review_data(self):
        response = export_reviews_csv([self.review])
        content = response.content.decode("utf-8")
        self.assertIn("Movie", content)
        self.assertIn("Test Movie", content)
        self.assertIn("8.5", content)
        self.assertIn("Great movie!", content)
        self.assertIn("Director", content)
        self.assertIn("2024", content)

    def test_export_empty_queryset(self):
        response = export_reviews_csv(Review.objects.none())
        content = response.content.decode("utf-8").strip()
        self.assertEqual(content, "media_type,title,rating,content,author,year")

    def test_export_multiple_reviews(self):
        Review.objects.create(
            user=self.user,
            title="Second Movie",
            media_type=MediaType.BOOK,
            rating=7.0,
            content="Good book",
            author="Author",
            year=2020,
        )
        response = export_reviews_csv(Review.objects.all().order_by("id"))
        content = response.content.decode("utf-8")
        lines = content.strip().split("\n")
        self.assertEqual(len(lines), 3)
        self.assertIn("Test Movie", content)
        self.assertIn("Second Movie", content)

    def test_export_sets_correct_content_type(self):
        response = export_reviews_csv(Review.objects.none())
        self.assertEqual(response["Content-Type"], "text/csv")

    def test_export_sets_content_disposition(self):
        response = export_reviews_csv(Review.objects.none())
        self.assertEqual(
            response["Content-Disposition"], "attachment; filename=reviews.csv"
        )


class ImportReviewsCsvTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="pass"
        )

    def _csv_file(self, content: str) -> io.BytesIO:
        return io.BytesIO(content.encode("utf-8"))

    def test_import_creates_review(self):
        csv_content = (
            f"{','.join(CSV_HEADERS)}\nMovie,New Film,7.5,Nice movie,Director,2024"
        )
        file = self._csv_file(csv_content)
        count, errors = create_reviews_from_csv(file, self.user)
        self.assertEqual(count, 1)
        self.assertEqual(errors, [])
        self.assertTrue(Review.objects.filter(title="New Film").exists())
        review = Review.objects.get(title="New Film")
        self.assertEqual(review.media_type, MediaType.MOVIE)
        self.assertEqual(str(review.rating), "7.5")

    def test_import_empty_file(self):
        csv_content = ",".join(CSV_HEADERS)
        file = self._csv_file(csv_content)
        count, errors = create_reviews_from_csv(file, self.user)
        self.assertEqual(count, 0)
        self.assertEqual(errors, [])

    def test_import_skips_header_row(self):
        csv_content = f"{','.join(CSV_HEADERS)}\nMovie,Real Film,7.0,Good,Writer,2023"
        file = self._csv_file(csv_content)
        count, errors = create_reviews_from_csv(file, self.user)
        self.assertEqual(count, 1)
        self.assertFalse(Review.objects.filter(title="media_type").exists())

    def test_import_invalid_year_logs_error(self):
        csv_content = f"{','.join(CSV_HEADERS)}\nMovie,Bad Year,7.5,Nice,Director,123"
        file = self._csv_file(csv_content)
        count, errors = create_reviews_from_csv(file, self.user)
        self.assertEqual(count, 0)
        self.assertEqual(len(errors), 1)
        self.assertIn("Bad Year", errors[0])

    def test_import_invalid_rating_logs_error(self):
        csv_content = (
            f"{','.join(CSV_HEADERS)}\nMovie,Bad Rating,15.0,Nice,Director,2024"
        )
        file = self._csv_file(csv_content)
        count, errors = create_reviews_from_csv(file, self.user)
        self.assertEqual(count, 0)
        self.assertEqual(len(errors), 1)
        self.assertIn("Bad Rating", errors[0])

    def test_import_duplicate_title_logs_error(self):
        Review.objects.create(
            user=self.user,
            title="Duplicate",
            media_type=MediaType.MOVIE,
            rating=8.0,
            content="Original",
            author="Author",
            year=2020,
        )
        csv_content = (
            f"{','.join(CSV_HEADERS)}\nMovie,Duplicate,7.0,Another,Writer,2021"
        )
        file = self._csv_file(csv_content)
        count, errors = create_reviews_from_csv(file, self.user)
        self.assertEqual(count, 0)
        self.assertEqual(len(errors), 1)

    def test_import_missing_field_logs_error(self):
        csv_content = (
            f"{','.join(CSV_HEADERS)}\nMovie,Missing Field,,Nice,Director,2024"
        )
        file = self._csv_file(csv_content)
        count, errors = create_reviews_from_csv(file, self.user)
        self.assertEqual(count, 0)
        self.assertEqual(len(errors), 1)

    def test_import_partial_success(self):
        Review.objects.create(
            user=self.user,
            title="First",
            media_type=MediaType.BOOK,
            rating=8.0,
            content="OK",
            author="A",
            year=2020,
        )
        csv_content = (
            f"{','.join(CSV_HEADERS)}\n"
            "Movie,First,7.0,Duplicate,Writer,2021\n"
            "Anime,Valid Anime,9.0,Great,Creator,2022"
        )
        file = self._csv_file(csv_content)
        count, errors = create_reviews_from_csv(file, self.user)
        self.assertEqual(count, 1)
        self.assertEqual(len(errors), 1)
        self.assertIn("First", errors[0])
        self.assertTrue(Review.objects.filter(title="Valid Anime").exists())
