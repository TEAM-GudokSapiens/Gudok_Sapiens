from django import forms
from django.db.models import fields
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.contrib.auth.hashers import check_password


class SignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)

        self.fields['user_id'].label = '아이디'
        self.fields['user_id'].widget.attrs.update({
            'class': 'form-control',
            'autofocus': False
        })
        self.fields['password1'].label = '비밀번호'
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
        })

    class Meta:
        model = get_user_model()
        fields = ('user_id', 'email', 'nickname', 'name',
                  'gender', 'phonenum', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['user_id'].label = '아이디'
        self.fields['user_id'].help_text = '20자 이하 문자, 숫자 그리고 @/./+/-/_만 가능합니다.'
        self.fields['email'].label = '이메일'
        self.fields['name'].label = '이름'
        self.fields['nickname'].label = '닉네임'
        self.fields['gender'].label = '성별'
        self.fields['phonenum'].label = '휴대폰 번호'
        self.fields['phonenum'].help_text = '-를 빼고 입력해주세요.'
        self.fields['password1'].help_text = '기호, 영어 소문자, 숫자를 혼합하여 10자리 이상'

    def save(self, commit=True):
        user = super(SignupForm, self).save(commit=False)
        user.level = '2'
        user.is_active = False
        user.save()

        return user


class UpdateForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('user_id', 'email', 'name', 'nickname',
                  'gender', 'phonenum', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['user_id'].label = '아이디'
        self.fields['user_id'].disabled = True
        self.fields['user_id'].help_text = False
        self.fields['email'].label = '이메일'
        self.fields['email'].disabled = True
        self.fields['name'].disabled = True
        self.fields['name'].label = '이름'
        self.fields['nickname'].label = '닉네임'
        self.fields['gender'].label = '성별'
        self.fields['gender'].disabled = True
        self.fields['phonenum'].label = '휴대폰 번호'
        self.fields['password1'].help_text = '기호, 영어 소문자, 숫자를 혼합하여 10자리 이상'


class LoginForm(forms.Form):
    user_id = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', }),
        error_messages={'required': '아이디을 입력해주세요.'},
        max_length=17,
        label='아이디'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', }),
        error_messages={'required': '비밀번호를 입력해주세요.'},
        label='비밀번호'
    )

    def clean(self):
        cleaned_data = super().clean()
        user_id = cleaned_data.get('user_id')
        password = cleaned_data.get('password')

        if user_id and password:
            try:
                user = User.objects.get(user_id=user_id)
            except User.DoesNotExist:
                self.add_error('user_id', '아이디가 존재하지 않습니다.')
                return

            if not check_password(password, user.password):
                self.add_error('password', '비밀번호가 틀렸습니다.')
