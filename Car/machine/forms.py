from django import forms
from .models import Comment
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        widgets = {
            "comment": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }


class RegisterForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control form-control-lg",
        "id": "form3Example4cg"
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control form-control-lg",
        "id": "form3Example4cdg"
    }))

    class Meta:
        model = User
        fields = ('username', 'email')
        widgets = {
            "username": forms.TextInput(attrs={
                "class": "form-control form-control-lg",
                "id": "form3Example1cg"
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control form-control-lg",
                "id": "form3Example3cg"
            })
        }


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        "class": "form-control",
        "id": "form2Example11"
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "id": "form2Example22"
    }))


class SendEmail(forms.Form):
    subject = forms.CharField(max_length=250, widget=forms.TextInput(attrs={
        "class": "form-control"
    }))
    message = forms.CharField(widget=forms.Textarea(attrs={
        "class": "form-control",
        "rows": 3
    }))