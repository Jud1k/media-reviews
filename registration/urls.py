from django.urls import path

from registration import views

app_name = "registration"

urlpatterns = [
    path("signup/", views.sign_up_user, name="signup"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
]
