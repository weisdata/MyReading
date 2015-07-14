from django import forms
from .models import Post
from django.contrib.auth.models import User
from .models import UserProfile

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'summary', 'image', 'link', 'source')


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')



class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')