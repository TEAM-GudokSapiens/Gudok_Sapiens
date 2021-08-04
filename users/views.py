from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import auth
from django.contrib.auth.models import User
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