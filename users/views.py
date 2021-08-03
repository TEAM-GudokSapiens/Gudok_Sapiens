from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth
from django.contrib.auth import login, logout, authenticate
from django.views import View
from .models import User
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect


def signup(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            user = User.objects.create_user(
                username=request.POST['email_id'],
                password=request.POST['password1'],
                email=request.POST['email_id'],
                name=request.POST['name'],
                nickname=request.POST['nickname'],
                phonenum=request.POST['phonenum'],
                gender=request.POST['gender'],
            )
            auth.login(request, user)
            return redirect('/')
        return render(request, 'users/signup.html')
    return render(request, 'users/signup.html')


class LoginView(View):
    def get(self, request):
        form = forms.LoginForm()  # forsm.py의 loginform을 받아와서 보여줘야
        ctx = {
            "form": form,  # form을 "form"으로 전달해줄겨
        }
        return render(request, "users/login.html", ctx)

    def post(self, request):
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            # cleand_data={'email':email@qowierj.com , 'password':qworf} 형태로 넘어오니가
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")

            user = authenticate(request, username=email, password=password)

            if user is not None:  # user가 있으면
                login(request, user)  # 로그인 /기본 django에 있는넘
                return render(request, "users/success.html")  # 로그인이 완료되면 이동
        return render(request, "users/login.html", {"form": form})
