
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User
from .models import UserProfile


# Verification form

from django import forms
from django.contrib.auth.forms import AuthenticationForm


class EmployeeAuthenticationForm(AuthenticationForm):

    username = forms.CharField(
        max_length=150,
        label="Username",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter your username",
                "autocomplete": "username",
                "autofocus": True,
            }
        )
    )

    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Enter your password",
                "autocomplete": "current-password",
            }
        )
    )

# Create employee form

class EmployeeCreateForm(forms.ModelForm):
    username = forms.CharField(max_length=150, label="Username")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    email = forms.EmailField(required=False, label="Email")

    profile_photo = forms.ImageField(
        required=False,
        label="Profile Photo",
        widget=forms.FileInput(
            attrs={
                'accept': 'image/jpeg,image/png,image/webp'
            }
        )
    )

    class Meta:
        model = UserProfile
        fields = [
            'first_name',
            'last_name',
            'position',
            'department',
            'phone',
            'mobile',
            'profile_photo',

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
        fields = ['first_name', 'last_name', 'position', 'department', 'phone', 'mobile', 'profile_photo']

        widgets = {
            'profile_photo': forms.FileInput(
                attrs={
                    'accept': 'image/jpeg,image/png,image/webp',
                    'id': 'id_profile_photo',
                    'style': 'display: none;',
                }
            ),
        }

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


