from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import EmailField

from authentication.models import User


class CustomAuthenticationForm(AuthenticationForm):
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                try:
                    user_temp = User.objects.get(email=username)
                except BaseException:
                    user_temp = None

                if user_temp is not None:
                    self.confirm_login_allowed(user_temp)
                else:
                    raise ValidationError(
                        self.error_messages['invalid_login'],
                        code='invalid_login',
                        params={'username': self.username_field.verbose_name},
                    )

        return self.cleaned_data


class RegisterForm(UserCreationForm):
    class Meta:
        fields = ("email",)
        field_classes = {'email': EmailField}
