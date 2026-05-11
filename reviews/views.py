from django.http import FileResponse, HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django_htmx.middleware import HtmxDetails
from django.views.decorators.http import require_GET, require_http_methods
from django.contrib import messages
from reviews.models import Review
from reviews.forms import ReviewCreateForm
from reviews.service import (
    create_reviews_from_csv,
    create_reviews_from_json,
    create_reviews_from_xlsx,
    get_reviews_csv,
    get_reviews_json,
    get_reviews_xlsx,
)
from django.contrib.auth.decorators import login_required
from django.db.models import QuerySet


class HtmxHttpRequest(HttpRequest):
    htmx: HtmxDetails


def _apply_review_filters(
    qs: QuerySet[Review],
    *,
    media_type: str | None,
    author: str | None,
    title: str | None,
    rating_min: str | None,
) -> QuerySet[Review]:
    if media_type:
        qs = qs.filter(media_type=media_type)
    if author:
        qs = qs.filter(author__icontains=author)
    if title:
        qs = qs.filter(title__icontains=title)
    if rating_min:
        try:
            rating_min_val = float(rating_min)
        except (TypeError, ValueError):
            rating_min_val = None
        if rating_min_val is not None:
            qs = qs.filter(rating__gte=rating_min_val)
    return qs


@require_GET
def index(request: HtmxHttpRequest) -> HttpResponse:
    if not request.user.is_authenticated:
        return render(request, "landing.html")
    return redirect("/reviews")


def create_review(request: HtmxHttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = ReviewCreateForm(request.POST)
        if form.is_valid():
            review: Review = form.save(commit=False)
            review.user = request.user
            review.save()

            if request.htmx:
                response = HttpResponse("")
                response["HX-Redirect"] = reverse("reviews:reviews")
                return response
            messages.success(request, "Review created successfuly!")
            return redirect("home")
        else:
            if request.htmx:
                response = render(
                    request, "reviews/partials/review_form.html", {"form": form}
                )
                response["HX-Retarget"] = "#review-form"
                response["HX-Reswap"] = "outerHTML"
                return response
            return redirect("home")
    else:
        form = ReviewCreateForm()
        if request.htmx:
            return render(
                request, "reviews/partials/review_create.html", {"form": form}
            )
        reviews = Review.objects.all()
    return render(
        request, "reviews/review_create_page.html", {"reviews": reviews, "form": form}
    )


ITEMS_PER_PAGE = 9


@login_required(login_url="/auth/login")
@require_GET
def list_review(request: HtmxHttpRequest) -> HttpResponse:
    media_type = (request.GET.get("media_type") or "").strip()
    author = (request.GET.get("author") or "").strip()
    title = (request.GET.get("title") or "").strip()
    rating_min = (request.GET.get("rating_min") or "").strip()

    try:
        page = max(1, int(request.GET.get("page", 1)))
    except (ValueError, TypeError):
        page = 1

    filtered_reviews = _apply_review_filters(
        Review.objects.select_related("user").all(),
        media_type=media_type or None,
        author=author or None,
        title=title or None,
        rating_min=rating_min or None,
    )

    total_count = filtered_reviews.count()
    total_pages = max(1, (total_count + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE)
    page = min(page, total_pages)

    start = (page - 1) * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE
    reviews = filtered_reviews[start:end]

    filters_dict = {
        "media_type": media_type,
        "author": author,
        "title": title,
        "rating_min": rating_min,
    }

    def build_base_url():
        params = []
        if media_type:
            params.append(f"media_type={media_type}")
        if author:
            params.append(f"author={author}")
        if title:
            params.append(f"title={title}")
        if rating_min:
            params.append(f"rating_min={rating_min}")
        return "?" + "&".join(params) if params else "?"

    page_range = list(range(1, total_pages + 1))
    base_url = build_base_url()

    context = {
        "reviews": reviews,
        "filters": filters_dict,
        "media_type_choices": Review._meta.get_field("media_type").choices,
        "current_page": page,
        "total_pages": total_pages,
        "page_range": page_range,
        "base_url": base_url,
    }

    if request.htmx:
        return render(request, "reviews/partials/review_list.html", context)
    return render(request, "reviews/review_page.html", context)


@login_required(login_url="/auth/login")
@require_http_methods(["DELETE"])
def delete_review(request: HtmxHttpRequest, pk: int) -> HttpResponse:
    try:
        review = Review.objects.get(pk=pk)
    except Review.DoesNotExist:
        return HttpResponse(status=404)
    if review.user_id != request.user.id:
        return HttpResponse(status=403)
    review.delete()
    response = HttpResponse()
    response["HX-Refresh"] = "true"
    return response


@login_required(login_url="/auth/login")
def edit_review(request: HtmxHttpRequest, pk: int) -> HttpResponse:
    try:
        review = Review.objects.get(pk=pk)
    except Review.DoesNotExist:
        return HttpResponse(status=404)
    if review.user_id != request.user.id:
        return HttpResponse(status=403)

    if request.method == "POST":
        form = ReviewCreateForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            response = HttpResponse()
            response["HX-Redirect"] = reverse("reviews:reviews")
            messages.success(request, "Review updated successfully!")
            return response
        else:
            response = render(
                request, "reviews/partials/review_form.html", {"form": form}
            )
            response["HX-Retarget"] = "#review-form"
            response["HX-Reswap"] = "outerHTML"
            return response
    else:
        form = ReviewCreateForm(instance=review)
        return render(
            request,
            "reviews/partials/review_edit.html",
            {"form": form, "action_url": f"/reviews/edit/{pk}"},
        )


@require_GET
def view_review(request: HtmxHttpRequest, pk: int) -> HttpResponse:
    try:
        review = Review.objects.select_related("user").get(pk=pk)
    except Review.DoesNotExist:
        return HttpResponse(status=404)
    if request.htmx:
        return render(request, "reviews/partials/review_view.html", {"review": review})
    return redirect("home")


@login_required(login_url="/auth/login")
def import_reviews(request: HtmxHttpRequest) -> HttpResponse:
    if request.method == "POST":
        file = request.FILES.get("file")
        filename = file.name
        if not file:
            messages.error(request, "No file provided")
            return redirect("reviews:reviews")
        if filename.endswith(".csv"):
            file_content = file.read().decode("utf-8")
            count, errors = create_reviews_from_csv(file_content, request.user)
        elif filename.endswith(".json"):
            file_content = file.read().decode("utf-8")
            count, errors = create_reviews_from_json(file_content, request.user)
        elif filename.endswith(".xlsx"):
            file_content = file
            count, errors = create_reviews_from_xlsx(file_content, request.user)
        else:
            messages.error(request, "Unsupported file format")
            return redirect("reviews:reviews")
        if errors:
            for error in errors:
                messages.error(request, error)
        messages.success(request, f"Imported {count} reviews")
        return redirect("reviews:reviews")
    return redirect("reviews:reviews")


@login_required(login_url="/auth/login")
@require_GET
def export_reviews(request: HtmxHttpRequest) -> HttpResponse:
    response = HttpResponse()
    file_format = request.GET.get("format")
    if not file_format:
        file_format = "csv"
    reviews = Review.objects.filter(user=request.user)
    if file_format == "csv":
        response = FileResponse(
            get_reviews_csv(reviews),
            as_attachment=True,
            content_type="text/csv",
        )
        response["Content-Disposition"] = 'attachment; filename="reviews.csv"'
        return response
    if file_format == "json":
        response = FileResponse(
            get_reviews_json(reviews),
            as_attachment=True,
            content_type="application/json",
        )
        response["Content-Disposition"] = 'attachment; filename="reviews.json"'
        return response
    if file_format == "xlsx":
        response = FileResponse(
            get_reviews_xlsx(reviews),
            as_attachment=True,
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = 'attachment; filename="reviews.xlsx"'
        return response
    return redirect("reviews:reviews")
