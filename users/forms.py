from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    """ Inherit from the UserCreationForm
    and modify it to include an email field """
    # https://docs.djangoproject.com/en/dev/topics/db/models/#meta-options
    # https://stackoverflow.com/questions/32860296/how-do-i-extend-usercreationform-to-include-email-field
    email = forms.EmailField(required=False)

    # The User model will be modified
    class Meta:
        model = User
        # This gives the order of the fields
        fields = ['username', 'email', 'password1', 'password2']
