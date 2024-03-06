from django import forms
from django.contrib.auth.models import User
from .models import UserProfile


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "password"]


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = "__all__"
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profileImage'].required = False
