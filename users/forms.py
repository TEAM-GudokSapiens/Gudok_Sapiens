from django import forms
from django.db.models import fields
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

# 회원 가입을 위한 form
class SignupForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username','email', 'nickname', 'name','gender','phonenum','password1', 'password2')