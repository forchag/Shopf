from django import forms
from django.utils.translation import gettext_lazy as _

from order.models import CouponModel


class AdminCouponForm(forms.ModelForm):
    class Meta:
        model = CouponModel
        fields = [
            "code",
            "discount_percent",
            "max_limit_usage",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["code"].widget.attrs["class"] = "form-control text-center"
        self.fields["code"].widget.attrs[
            "placeholder"
        ] = _("Enter the discount code")
        self.fields["discount_percent"].widget.attrs[
            "class"
        ] = "form-control text-center"
        self.fields["discount_percent"].widget.attrs[
            "placeholder"
        ] = _("Discount amount")
        self.fields["max_limit_usage"].widget.attrs[
            "class"
        ] = "form-control text-center"
        self.fields["max_limit_usage"].widget.attrs[
            "placeholder"
        ] = _("Maximum usage")
