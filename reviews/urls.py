from reviews import views
from django.urls import path

app_name = "reviews"

urlpatterns = [
    path("", views.list_review, name="reviews"),
    path("new/", views.create_review, name="review-create"),
    path("view/<int:pk>", views.view_review, name="review-view"),
    path("edit/<int:pk>", views.edit_review, name="review-edit"),
    path("import/", views.import_reviews, name="review-import"),
    path("export/", views.export_reviews, name="review-export"),
    path("<int:pk>", views.delete_review, name="review-delete"),
]
