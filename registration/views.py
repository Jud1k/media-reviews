from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import login, logout
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.views.decorators.http import require_POST
from registration.forms import SignupForm, LoginForm
from reviews.views import HtmxHttpRequest


@require_http_methods(["POST", "GET"])
def sign_up_user(request: HtmxHttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            if request.htmx:
                response = HttpResponse()
                response["HX-Redirect"] = reverse("home")
            else:
                response = redirect("home")
            return response
        elif request.htmx:
            return render(request, "registration/signup_form.html", {"form": form})
        return render(request, "registration/signup_form.html", {"form": form})
    else:
        form = SignupForm()
        return render(request, "registration/signup.html", {"form": form})


@require_http_methods(["POST", "GET"])
def login_user(request: HtmxHttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if request.htmx:
                response = HttpResponse()
                response["HX-Redirect"] = reverse("home")
            else:
                response = redirect("home")
            return response
        elif request.htmx:
            return render(request, "registration/login_form.html", {"form": form})
        return render(request, "registration/login.html", {"form": form})
    else:
        form = LoginForm()
        return render(request, "registration/login.html", {"form": form})

@require_POST
def logout_user(request:HtmxHttpRequest) -> HttpResponse:
    logout(request)
    response = HttpResponse()
    response["HX-Redirect"] = reverse("home")
    return response