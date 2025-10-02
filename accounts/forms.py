from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

class SignupForm(forms.Form):
    full_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your full name', 'class': 'form-control'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'example@mail.com', 'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Create a strong password', 'class': 'form-control'})
    )
    confirm_age = forms.BooleanField(required=True)

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already registered.")
        return email

    def clean_password(self):
        pw = self.cleaned_data['password']
        if len(pw) < 6:
            raise forms.ValidationError("Password must be at least 6 characters.")
        return pw

class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Email address', 'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'})
    )
