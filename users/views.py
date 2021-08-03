from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import auth
from django.contrib.auth import login,authenticate
from .models import User


def signup(request):
    if request.method == "POST":
        if request.POST['password1'] == request.POST['password2']:
            user = User.objects.create_user(
                email=request.POST['email_id'],
                name = request.POST['name'], 
                password=request.POST['password1'],
                phonenum=request.POST['phonenum'],
                gender=request.POST['gender'],
                created_at=request.POST['created_at'],
            )
            auth.login(request, user)
            return redirect('/')
        return render(request, 'users/signup.html')
    return render(request, 'users/signup.html')