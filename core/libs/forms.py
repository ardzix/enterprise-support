'''
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# File: form.py
# Project: core.lakon.app
# File Created: Friday, 7th September 2018 3:50:58 am
#
# Author: Arif Dzikrullah
#         ardzix@hotmail.com>
#         https://github.com/ardzix/>
#
# Last Modified: Friday, 7th September 2018 3:51:22 am
# Modified By: arifdzikrullah (ardzix@hotmail.com>)
#
# Hand-crafted & Made with Love
# Copyright - 2018 Lakon, lakon.app
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''


import nexmo
import uuid
from django.conf import settings
from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList
from django.contrib.auth.forms import *
from django.forms import *
from django.contrib.auth import get_user_model
from django.utils.translation import gettext, gettext_lazy as _
from .nonce import NonceObject


class ErrorDiv(ErrorList):
    def __str__(self):
        return self.as_divs()

    def __unicode__(self):
        return self.as_divs()

    def as_divs(self):
        if not self:
            return ''
        else:
            errors = ''.join(['<div class="error">%s</div>' % e for e in self])
            return '<div class="errors">%s</div>' % errors


class AuthForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(AuthForm, self).__init__(*args, **kwargs)

        self.error_class = ErrorDiv

        self.fields["username"].widget.attrs = {
            "class": "form-control"
        }

        self.fields["password"].widget.attrs = {
            "class": "form-control"
        }

        self.fields["username"].label = "Phone number"


class NewPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(NewPasswordForm, self).__init__(*args, **kwargs)

        self.error_class = ErrorDiv

        self.fields["new_password1"].widget.attrs = {
            "class": "form-control"
        }
        self.fields["new_password2"].widget.attrs = {
            "class": "form-control"
        }


class ChangePasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

        self.error_class = ErrorDiv

        self.fields["old_password"].widget.attrs = {
            "class": "form-control"
        }
        self.fields["new_password1"].widget.attrs = {
            "class": "form-control"
        }
        self.fields["new_password2"].widget.attrs = {
            "class": "form-control"
        }


class RegisterForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("email",)

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        self.error_class = ErrorDiv

        self.fields["email"].widget.attrs = {
            "class": "form-control"
        }

        self.fields["password1"].widget.attrs = {
            "class": "form-control"
        }
        self.fields["password1"].required = False

        self.fields["password2"].widget.attrs = {
            "class": "form-control"
        }
        self.fields["password2"].required = False


class NonceModelForm(ModelForm):
    def save(self, created_by=None, commit=True):
        if not hasattr(self, 'cleaned_data'):
            raise ValidationError({'detail': 'Please validate before saving'})

        if 'nonce' not in self.cleaned_data:
            if not self.instance.nonce:
                self.instance.nonce = str(uuid.uuid4())

        if created_by:
            self.instance.created_by = created_by

        return super(NonceModelForm, self).save(commit=commit)
