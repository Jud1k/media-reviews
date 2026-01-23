from reviews import views
from django.urls import path

app_name = "reviews"

urlpatterns = [
    path("", views.list_review, name="reviews"),
    path("new/", views.create_review, name="review-create"),
]
