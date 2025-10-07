from django import forms
from django.utils.translation import gettext_lazy as _

from order.models import AddressModel, CouponModel


class CheckOutForm(forms.Form):
    address_id = forms.IntegerField(required=True)
    coupon_code = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(CheckOutForm, self).__init__(*args, **kwargs)

    def clean_address_id(self):
        address_id = self.cleaned_data.get("address_id")
        try:
            address = AddressModel.objects.get(
                id=address_id, user=self.request.user
            )
        except AddressModel.DoesNotExist:
            raise forms.ValidationError(_("The address does not match the current user."))

        return address

    def clean_coupon_code(self):
        coupon_code = self.cleaned_data.get("coupon_code")
        coupon = None
        if coupon_code == "":
            return coupon

        try:
            coupon = CouponModel.objects.get(code=coupon_code)
        except CouponModel.DoesNotExist:
            raise forms.ValidationError(_("The code you entered is incorrect."))

        if coupon:
            if self.request.user in coupon.used_by.all():
                raise forms.ValidationError(
                    _("You have already used this code once.")
                )
            if coupon.max_limit_usage == 0:
                raise forms.ValidationError(_("This code is no longer valid."))
        return coupon
