from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth import get_user_model


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = get_user_model()
        fields = ('username', 'email',)


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserCreationForm):
        model = get_user_model()
        fields = ('username', 'email')


class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta(UserChangeForm):
        model = get_user_model()
        fields = ('old_password', 'new_password1', 'new_password2',)