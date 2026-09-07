
from django import forms
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User
from .models import UserProfile

class EmployeeCreateForm(forms.ModelForm):
    username = forms.CharField(max_length=150, label="Потребителско име")
    password = forms.CharField(widget=forms.PasswordInput, label="Парола")
    email = forms.EmailField(required=False, label="Имейл")

    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'position', 'department', 'phone']

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


class EmployeeUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=False, label="Имейл")

    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'position', 'department', 'phone']

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