from django.contrib.auth import views
from django.contrib.auth.forms import AuthenticationForm

from authentication.forms import CustomAuthenticationForm


class CustomLoginView(views.LoginView):
    template_name = 'registration/login.html'
    form_class = CustomAuthenticationForm


class CustomLogoutView(views.LogoutView):
    template_name = 'registration/logout.html'
