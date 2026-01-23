from django.urls import path

from registration import views

app_name = "registration"

urlpatterns = [
    path("signup/", views.sign_up, name="signup"),
]
