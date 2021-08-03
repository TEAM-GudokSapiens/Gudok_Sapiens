from django import forms
from django.core.exceptions import ValidationError
from . import models

class LoginForm(forms.Form):
    email=forms.EmailField()
    password=forms.CharField(widget=forms.PasswordInput) 
    # 비번누를 때 입력하는거 가려지는거

    #유효성 검증: clean_*** 로 만들기
    
    #email, password 같이 검증
    def clean(self):
        email=self.cleaned_data.get("email") #email 가져옴 => 오류가 없으면 null
        password=self.cleaned_data.get("password") #password 가져옴 => 오류가 없으면 null
        try:
            user=models.User.objects.get(username=email)
            if user.check_password(password): 
                return self.cleaned_data
            else:
                raise forms.ValidationError("password is wrong")
        except models.User.DoesNotExist:
            raise forms.ValidationError("user does not exist!")



