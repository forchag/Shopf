from django.contrib import messages
from django.contrib.auth import login, views as auth_views
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView

from .forms import CustomAuthenticationForm, RegistrationForm


class SignUpView(SuccessMessageMixin, CreateView):
    template_name = "accounts/signup.html"
    form_class = RegistrationForm
    success_message = _("User registration completed successfully")
    success_url = reverse_lazy("website:home")

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.instance
        login(self.request, user)
        return response


class LoginView(SuccessMessageMixin, auth_views.LoginView):
    template_name = "accounts/login.html"
    form_class = CustomAuthenticationForm
    redirect_authenticated_user = True
    success_message = _("Signed in successfully")


class LogoutView(auth_views.LogoutView):
    next_page = reverse_lazy("website:home")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.success(request, _("Signed out successfully"))
        return super().dispatch(request, *args, **kwargs)
