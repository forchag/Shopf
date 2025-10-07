from django import forms
from django.utils.translation import gettext_lazy as _

from .models import ReviewModel


class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewModel
        fields = ["product", "rate", "description"]

        error_messages = {
            "description": {
                "required": _("The description field is required."),
            },
        }
