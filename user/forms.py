from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['fullname', 'location']