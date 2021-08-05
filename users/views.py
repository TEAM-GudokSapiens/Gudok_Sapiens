from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from .forms import SignupForm
from .models import User
from django.views.generic import UpdateView, DeleteView
from users.forms import UpdateForm


# 회원가입


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('users:login')
    else:
        form = SignupForm()
    ctx = {'form': form}
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

# 유저정보


class UpdateView(UpdateView):
    model = User
    context_object_name = 'target_user'
    form_class = UpdateForm
    success_url = reverse_lazy('services:main')
    template_name = 'users/detail.html'

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return super().get(*args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('users:login'))

    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return super().get(*args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('users:login'))

# 회원탈퇴


class DeleteView(DeleteView):
    model = User
    context_object_name = 'target_user'
    success_url = reverse_lazy('users:login')
    template_name = 'users/delete.html'

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return super().get(*args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('users:login'))

    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return super().get(*args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('users:login'))
