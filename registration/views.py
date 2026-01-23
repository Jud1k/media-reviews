from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.views.decorators.http import require_http_methods

from registration.forms import SignupForm
from reviews.views import HtmxHttpRequest

# Create your views here.

@require_http_methods(["POST","GET"])
def sign_up(request: HtmxHttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
        return render(request,"registration/signup.html",{"form":form})
    else:
        form = SignupForm()
    return render(request, "registration/signup.html", {"form": form})
