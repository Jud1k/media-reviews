import datetime
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse


class MediaType(models.TextChoices):
    BOOK = "book", "Книга"
    MOVIE = "movie", "Фильм"
    ANIME = "anime", "Аниме"
    SERIES = "series", "Сериал"
    GAME = "game", "Игра"
    MUSIC = "music", "Альбом"
    OTHER = "other", "Другое"


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    media_type = models.CharField(
        max_length=20, choices=MediaType.choices, verbose_name="Name media"
    )
    title = models.CharField(max_length=200, verbose_name="Name of work")
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        verbose_name="Rating (1-10)",
        validators=[MinValueValidator(1.0), MaxValueValidator(10.0)],
    )
    content = models.TextField(verbose_name="Review")
    author = models.CharField(max_length=100, verbose_name="Author")
    year = models.PositiveSmallIntegerField(
        verbose_name="Year of release",
        validators=[
            MinValueValidator(868),
            MaxValueValidator(datetime.date.today().year),
        ],
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Review"
        verbose_name_plural = "Reviews"

    def get_absolute_url(self):
        return reverse("review-detail", args=[self.pk])

    def get_rating_color(self):
        """Color for display rating"""
        if self.rating >= 8:
            return "text-green-600"
        elif self.rating >= 6:
            return "text-yellow-600"
        else:
            return "text-red-600"
