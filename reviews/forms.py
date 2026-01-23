from django import forms

from reviews.models import Review


class ReviewCreateForm(forms.ModelForm):
    """A form for creating review model"""

    class Meta:
        model = Review
        fields = ["title", "media_type", "author", "year", "rating", "content"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "input-field",
                    "placeholder": "Title of the book/movie...",
                }
            ),
            "media_type": forms.Select(attrs={"class": "select-field"}),
            "rating": forms.NumberInput(
                attrs={
                    "class": "input-field",
                    "min": "0",
                    "max": "10",
                    "step": "0.5",
                    "placeholder": "0-10",
                }
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "textarea-field",
                    "rows": 4,
                    "placeholder": "Write your review here...",
                }
            ),
        }
