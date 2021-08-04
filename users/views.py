from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from .forms import SignupForm
from .models import User

# 회원가입
def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('users:login')
    else:
        form = SignupForm()
    ctx={'form' : form}
    return render(request, template_name="users/signup.html", context=ctx)

# 로그인
def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('services:main')
        else:
            return render(request, 'users/login.html', {'error': 'username or password is incorrect'})
    else:
        return render(request, 'users/login.html')

# 로그아웃   
def logout(request):
    auth.logout(request)
    return redirect('services:main')

#유저정보
def detail(request, pk):
    return render(request, 'users/detail.html')

#비밀번호 바꾸기
def change_pw(request):
    context= {}
    if request.method == "POST":
        current_password = request.POST.get("origin_password")
        user = request.user
        if check_password(current_password,user.password):
            new_password = request.POST.get("password1")
            password_confirm = request.POST.get("password2")
            if new_password == password_confirm: #변경성공
                user.set_password(new_password)
                user.save()
                auth.login(request,user)
                return redirect("services:main")
            else:
                context.update({'error':"새로운 비밀번호를 다시 확인해주세요."})
    else:
        context.update({'error':"현재 비밀번호가 일치하지 않습니다."})
    
    return render(request, 'users/change_pw.html',context)
