from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django_htmx.middleware import HtmxDetails
from django.views.decorators.http import require_GET
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from reviews.models import Review
from reviews.forms import ReviewCreateForm

class HtmxHttpRequest(HttpRequest):
    htmx: HtmxDetails

@require_GET
def index(request:HtmxHttpRequest)->HttpResponse:
    return redirect('reviews:reviews')

def create_review(request:HtmxHttpRequest)->HttpResponse:
    if request.method=="POST":
        form = ReviewCreateForm(request.POST)
        if form.is_valid():
            review:Review = form.save(commit=False)
            review.user = request.user
            review.save()
            
            if request.htmx:
                return render(request,'reviews/review_card.html',{"review":review})
            messages.success(request,'Review created successfuly!')
            return redirect('home')
        else:
            if request.htmx:
                return render(request,'reviews/review_create.html',{"form":form})
            return redirect('home')
    else:
        form = ReviewCreateForm()
        if request.htmx:
            return render(request,'reviews/review_create.html',{'form':form,'modal':True})
    return render(request,'reviews/index.html')

@require_GET
def list_review(request:HtmxHttpRequest)->HttpResponse:
    reviews = Review.objects.all()
    
    if request.htmx:
        return render(request,'reviews/index.html',{'reviews':reviews})
    
    return render(request,'reviews/index.html',{'reviews':reviews})
