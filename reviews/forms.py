from django import forms
from reviews.models import Review


class ReviewCreateForm(forms.ModelForm):
    """A form for creating review model"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Review
        fields = ["title", "media_type", "author", "year", "rating", "content"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition-all",
                    "placeholder": "The Lord of the Rings, Inception...",
                }
            ),
            "media_type": forms.Select(
                attrs={
                    "class": "w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition-all appearance-none",
                }
            ),
            "author": forms.TextInput(
                attrs={
                    "class": "w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition-all",
                    "placeholder": "J.R.R. Tolkien, Christopher Nolan...",
                }
            ),
            "year": forms.NumberInput(
                attrs={
                    "class": "w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition-all",
                    "placeholder": "2026",
                    "min": "1900",
                    "max": "2026",
                    "step": "1",
                }
            ),
            "rating": forms.NumberInput(
                attrs={
                    "class": "w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition-all",
                    "placeholder": "8.5",
                    "min": "0",
                    "max": "10",
                    "step": "0.5",
                }
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition-all resize-none",
                    "rows": 5,
                    "placeholder": "Share your thoughts... What did you like or dislike?",
                }
            ),
        }
