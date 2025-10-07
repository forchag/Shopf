from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import UpdateView, View

from accounts.models import Profile, UserType


class DashboardCheckView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        user_type = request.user.user_type
        if user_type == UserType.customer.value:
            return redirect(reverse_lazy("dashboard:customer:home"))
        elif user_type == UserType.admin.value:
            return redirect(reverse_lazy("dashboard:admin:home"))
        return super().dispatch(request, *args, **kwargs)


class ProfileEditView(UpdateView, SuccessMessageMixin):
    http_method_names = ["post"]
    model = Profile
    fields = ["avatar"]
    success_url = reverse_lazy("dashboard:check")
    success_message = _("Your profile picture has been updated successfully")

    def get_object(self, queryset=None):
        return Profile.objects.get(user=self.request.user)
