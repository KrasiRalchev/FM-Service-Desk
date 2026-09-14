
from django import forms
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User
from .models import UserProfile

from django.contrib.auth import authenticate


# Verification form

class EmployeeVerificationForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        label="Username"
    )

    password = forms.CharField(
        widget=forms.PasswordInput,
        label="Password"
    )

    def clean(self):
        cleaned_data = super().clean()

        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:
            user = authenticate(
                username=username,
                password=password
            )

            if user is None:
                raise forms.ValidationError(
                    "Invalid username or password."
                )

            cleaned_data["user"] = user

        return cleaned_data

# Create employee form

class EmployeeCreateForm(forms.ModelForm):
    username = forms.CharField(max_length=150, label="Username")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    email = forms.EmailField(required=False, label="Email")

    class Meta:
        model = UserProfile
        fields = [
            'first_name',
            'last_name',
            'position',
            'department',
            'phone',
            'mobile'
        ]

    def clean_username(self):
        username = self.cleaned_data['username']

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                "This username already exists."
            )

        return username

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'],
            email=self.cleaned_data.get('email', '')
        )

        profile = super().save(commit=False)
        profile.user = user

        if commit:
            profile.save()

        return profile


# Update employee form

class EmployeeUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=False, label="Email")

    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'position', 'department', 'phone', 'mobile']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['email'].initial = self.instance.user.email

    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            profile.save()
            # Обновяваме и имейла на User
            profile.user.email = self.cleaned_data.get('email', '')
            profile.user.save()
        return profile


class EmployeePasswordChangeForm(SetPasswordForm):
    class Meta:
        fields = ['new_password1', 'new_password2']


