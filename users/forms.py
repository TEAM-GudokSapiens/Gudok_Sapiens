from django import forms
from django.db.models import fields
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class SignupForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'nickname', 'name',
                  'gender', 'phonenum', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].label = '아이디'
        self.fields['username'].help_text = '20자 이하 문자, 숫자 그리고 @/./+/-/_만 가능합니다.'
        self.fields['email'].label = '이메일'
        self.fields['name'].label = '이름'
        self.fields['nickname'].label = '닉네임'
        self.fields['gender'].label = '성별'
        self.fields['phonenum'].label = '휴대폰 번호'
        self.fields['password1'].help_text = '기호, 영어 소문자, 숫자를 혼합하여 10자리 이상'


class UpdateForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'name', 'nickname',
                  'gender', 'phonenum', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].label = '아이디'
        self.fields['username'].disabled = True
        self.fields['username'].help_text = False
        self.fields['email'].label = '이메일'
        self.fields['email'].disabled = True
        self.fields['name'].disabled = True
        self.fields['name'].label = '이름'
        self.fields['nickname'].label = '닉네임'
        self.fields['gender'].label = '성별'
        self.fields['gender'].disabled = True
        self.fields['phonenum'].label = '휴대폰 번호'
        self.fields['password1'].help_text = '기호, 영어 소문자, 숫자를 혼합하여 10자리 이상'
