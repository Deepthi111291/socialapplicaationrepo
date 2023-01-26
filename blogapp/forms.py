from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from blogapp.models import UserProfile,Blogs,Comments

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model=User
        fields=[
            "first_name",
            "last_name",
            "email",
            "username",
            "password1",
            "password2"
        ]

class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput())

class UserProfileForm(ModelForm):
    class Meta:
        model=UserProfile
        exclude=('user',)            #get everything from model except user
        widgets={
            "date_of_birth":forms.DateInput(attrs={"class":"form-control","type":"date"})
        }

class PasswordResetForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password=forms.CharField()

class BlogForm(ModelForm):
    class Meta:
        model=Blogs
        fields=["title","description","image"]
        widgets={
            "title":forms.TextInput(attrs={"class":"form-control"}),
            "description":forms.Textarea(attrs={"class":"form-control"}),
            "image":forms.FileInput(attrs={"class":"form-control"})
        }

class CommentForm(ModelForm):                     #CommentForm inherited from ModelForm
    class Meta:
        model=Comments
        fields=["comment"]
        widgets={
            "comment":forms.TextInput(attrs={"class":"form-control"})
        }


    # deeps
    # Janki@050320
