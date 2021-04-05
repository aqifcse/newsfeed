from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

class UserAuthForm(AuthenticationForm):
    
    error_messages = {
        'invalid_login': _("Incorrect username or password"),
        'invalid': _("Invalid user input!"),
        'inactive': _("This account is inactive."),
    }

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                if self.user_cache:
                    self.confirm_login_allowed(self.user_cache)
                else:
                    raise forms.ValidationError(
                        self.error_messages['invalid'],
                        code='invalid',
                    )

        return self.cleaned_data

class EmailValidationOnForgotPassword(PasswordResetForm):

    error_messages = {
        'unregistered': _("The email is not registered. Please register"),
    }

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            raise forms.ValidationError(self.error_messages['unregistered'], code='unregistered',)

        return email