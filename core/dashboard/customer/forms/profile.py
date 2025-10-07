from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.translation import gettext_lazy as _

from accounts.models import Profile


class ChangePassForm(PasswordChangeForm):
    pass


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["first_name", "last_name", "phone_number"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs["class"] = "form-control"
        self.fields["last_name"].widget.attrs["class"] = "form-control"
        self.fields["phone_number"].widget.attrs[
            "class"
        ] = "form-control text-center"
        self.fields["first_name"].widget.attrs[
            "placeholder"
        ] = _("Enter your first name")
        self.fields["last_name"].widget.attrs[
            "placeholder"
        ] = _("Enter your last name")
        self.fields["phone_number"].widget.attrs[
            "placeholder"
        ] = _("Enter your phone number")
