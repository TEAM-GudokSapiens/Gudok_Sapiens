from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from .forms import SignupForm
from .models import User
from django.views.generic import UpdateView, DeleteView
from users.forms import UpdateForm
from .forms import LoginForm
from django.contrib.auth import login, authenticate
from django.views.generic import FormView
from django.utils.decorators import method_decorator
from .decorators import *
from django.contrib.auth import logout


# 회원가입


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")
            return redirect('services:main')
    else:
        form = SignupForm()
    ctx = {'form': form}
    return render(request, template_name="users/signup.html", context=ctx)

# 로그인


@method_decorator(logout_message_required, name='dispatch')
class LoginView(FormView):
    template_name = 'users/login.html'
    form_class = LoginForm
    success_url = '/services/main/'

    def form_valid(self, form):
        user_id = form.cleaned_data.get("user_id")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=user_id, password=password)

        if user is not None:
            self.request.session['user_id'] = user_id
            login(self.request, user,
                  backend="django.contrib.auth.backends.ModelBackend")

        return super().form_valid(form)
# 로그아웃


def logout_view(request):
    logout(request)
    return redirect('/')

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
