from django.contrib.auth import views
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.generic import FormView

from authentication import tasks
from authentication.forms import CustomAuthenticationForm, RegisterForm
from authentication.models import User


class CustomLoginView(views.LoginView):
    template_name = 'registration/login.html'
    form_class = CustomAuthenticationForm


class CustomLogoutView(views.LogoutView):
    template_name = 'registration/logout.html'


class RegisterView(FormView):
    template_name = ''
    form_class = RegisterForm

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            user = User.objects.get()
            context = {
                'link': build_url(scheme=self.request.scheme,
                                  uid=urlsafe_base64_encode(force_bytes(user.id)),
                                  token=default_token_generator.make_token(user),
                                  path=ACTIVATION_PATH)
            }
            tasks.send_email.delay(subject="email/activate_account_subject.txt",
                                   template="email/activate_account.html",
                                   emails=[email], context=context)
