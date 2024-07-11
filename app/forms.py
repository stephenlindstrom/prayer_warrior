from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from .models import PrayerRequest

class PrayerRequestForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        forms.ModelForm.__init__(self, *args, **kwargs)
        self.fields['groups'].queryset = Group.objects.filter(user=user)


    groups = forms.ModelMultipleChoiceField(queryset=Group.objects.none(), label="Groups", required=False)
    class Meta:
        model = PrayerRequest
        fields = ["content"]

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]


class AddMemberForm(forms.Form):
    username = forms.CharField()
