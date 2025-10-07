from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import DeleteView, ListView

from shop.models import WishListModel

from ...permissions import CustomerPermissions
from ..forms import *


class WishListView(LoginRequiredMixin, CustomerPermissions, ListView):
    template_name = "dashboard/customer/wishlist/wishlist.html"
    context_object_name = "wishes"

    paginate_by = 1

    def get_queryset(self):
        return WishListModel.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["wish_number"] = len(self.get_queryset())
        return context


class DeleteWishView(
    LoginRequiredMixin, CustomerPermissions, SuccessMessageMixin, DeleteView
):
    http_method_names = ["post"]
    success_url = reverse_lazy("dashboard:customer:wishlist")
    success_message = _("Product removed from wishlist")

    def get_queryset(self):
        return WishListModel.objects.filter(user=self.request.user)
