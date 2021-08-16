from django.shortcuts import render, redirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.forms.utils import ErrorList
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView, DeleteView, FormView, CreateView, View
from services.models import Service
from reviews.models import Review
from django.core.paginator import Paginator
from django.contrib.auth.tokens import PasswordResetTokenGenerator, default_token_generator
from django.core.exceptions import PermissionDenied
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect, Http404, HttpResponseForbidden, HttpResponse, JsonResponse
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text
from django.urls import reverse
from .helper import send_mail, email_auth_num
from .forms import CustomSetPasswordForm
import json
import os
import requests
from django.template import loader
from django.core.serializers.json import DjangoJSONEncoder
from .forms import *
from .models import *
from .decorators import *
from .exception import *


# 회원가입
class Signup(CreateView):
    model = User
    template_name = 'users/signup.html'
    form_class = SignupForm

    def get(self, request, *args, **kwargs):
        if not request.session.get('agreement', False):
            raise PermissionDenied
        request.session['agreement'] = False
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        self.request.session['register_auth'] = True
        messages.success(
            self.request, '회원님의 입력한 Email 주소로 인증 메일이 발송되었습니다. 인증 후 로그인이 가능합니다.')
        return reverse('users:register_success')


        send_mail(
            '{}님의 회원가입 인증메일 입니다.'.format(self.object.user_id),
            recipient_list=[self.object.email],
            from_email='david90907@naver.com',
            message='',
            html_message=render_to_string('users/register_email.html', {
                'user': self.object,
                'uid': urlsafe_base64_encode(force_bytes(self.object.pk)).encode().decode(),
                'domain': self.request.META['HTTP_HOST'],
                'token': default_token_generator.make_token(self.object),
            }),
        )
        return redirect(self.get_success_url())


# 회원가입 인증메일 발송 안내 창
def register_success(request):
    if not request.session.get('register_auth', False):
        raise PermissionDenied
    request.session['register_auth'] = False

    return render(request, 'users/register_success.html')


# 이메일 인증 성공시 자동로그인
def activate(request, uid64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uid64))
        current_user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist, ValidationError):
        messages.error(request, '메일 인증에 실패했습니다.')
        return redirect('users:login')

    if default_token_generator.check_token(current_user, token):
        current_user.is_active = True
        current_user.save()

        messages.info(request, '메일 인증이 완료 되었습니다. 회원가입을 축하드립니다!')
        return redirect('users:login')

    messages.error(request, '메일 인증에 실패했습니다.')
    return redirect('users:login')


# 로그인
@method_decorator(logout_message_required, name='dispatch')
class LoginView(FormView):
    template_name = 'users/login.html'
    form_class = LoginForm
    success_url = '/services/main/'
    ctx = {}

    def form_valid(self, form):
        user_id = form.cleaned_data.get("user_id")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=user_id, password=password)

        if user is not None:
            self.request.session['user_id'] = user_id
            if user.is_active:
                login(self.request, user)
            else:
                ctx.update(
                    {'messages': "회원님의 입력한 Email 주소로 인증 메일이 발송되었습니다. 인증 후 로그인이 가능합니다."})
                return render(self.request, 'users/login.html', ctx)

        return super().form_valid(form)


# 로그아웃
def logout_view(request):
    logout(request)
    return redirect('/')


# 유저정보
class AccountUpdateView(UpdateView):
    model = User
    form_class = UpdateForm
    success_url = reverse_lazy('services:main')
    template_name = 'users/update.html'

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated and self.get_object() == self.request.user:
            return super().get(*args, **kwargs)
        else:
            return HttpResponseForbidden()

    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated and self.get_object() == self.request.user:
            return super().post(*args, **kwargs)
        else:
            return HttpResponseForbidden()


# 비밀번호 변경
@login_message_required
def update_password(request):
    if request.method == 'POST':
        password_change_form = PasswordChangeForm(request.user, request.POST)
        if password_change_form.is_valid():
            user = password_change_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "비밀번호를 성공적으로 변경하였습니다.")
            return redirect('services:main')
    else:
        password_change_form = PasswordChangeForm(request.user)

    return render(request, 'users/update_password.html', {'password_change_form': password_change_form})


# 회원탈퇴
@login_message_required
def profile_delete_view(request):
    if request.method == 'POST':
        password_form = CheckPasswordForm(request.user, request.POST)

        if password_form.is_valid():
            request.user.delete()
            logout(request)
            messages.success(request, "회원탈퇴가 완료되었습니다.")
            return redirect('/users/login/')
    else:
        password_form = CheckPasswordForm(request.user)

    return render(request, 'users/delete.html', {'password_form': password_form})


def dibs_list(request):
    services_list = Service.objects.filter(dib__users=request.user.id)
    # 한 페이지 당 담을 수 있는 객체 수를 정할 수 있음
    paginator = Paginator(services_list, 10)
    page = request.GET.get('page')
    services = paginator.get_page(page)

    ctx = {
        'services': services,
    }
    return render(request, 'users/dibs_list.html', context=ctx)


def reviews_list(request):
    reviews_list = Review.objects.filter(user=request.user.id)
    # 한 페이지 당 담을 수 있는 객체 수를 정할 수 있음
    paginator = Paginator(reviews_list, 10)
    page = request.GET.get('page')
    reviews = paginator.get_page(page)

    ctx = {
        'reviews': reviews,
    }
    return render(request, 'users/reviews_list.html', context=ctx)


# 이용약관 동의
@method_decorator(logout_message_required, name='dispatch')
class AgreementView(View):
    def get(self, request, *args, **kwargs):
        request.session['agreement'] = False
        return render(request, 'users/agreement.html')

    def post(self, request, *args, **kwarg):
        if request.POST.get('agreement1', False) and request.POST.get('agreement2', False) and request.POST.get('register') == 'register':
            request.session['agreement'] = True
            return redirect('/users/signup/')

        else:
            messages.info(request, "약관에 모두 동의해주세요.")
            return render(request, 'users/agreement.html')

# 아이디 찾기

# 아이디 찾기
@method_decorator(logout_message_required, name='dispatch')
class RecoveryIdView(View):
    template_name = 'users/recovery_id.html'
    recovery_id = RecoveryIdForm

    def get(self, request):
        if request.method == 'GET':
            form = self.recovery_id(None)
        return render(request, self.template_name, {'form': form, })


def ajax_find_id_view(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    result_id = User.objects.get(name=name, email=email)

    return HttpResponse(json.dumps({"result_id": result_id.user_id}, cls=DjangoJSONEncoder), content_type="application/json")

# 비밀번호찾기


@method_decorator(logout_message_required, name='dispatch')
class RecoveryPwView(View):
    template_name = 'users/recovery_pw.html'
    recovery_pw = RecoveryPwForm

    def get(self, request):
        if request.method == 'GET':
            form_pw = self.recovery_pw(None)
            return render(request, self.template_name, {'form_pw': form_pw, })


    return render(request, 'users/password_reset.html', {'form': reset_password_form})
        reset_password_form = CustomSetPasswordForm(request.user)

    else:
            request.session['auth'] = session_user
        else:
            logout(request)
            return redirect('users:login')
            logout(request)
            messages.success(request, "비밀번호 변경완료! 변경된 비밀번호로 로그인하세요.")
            user = reset_password_form.save()
        if reset_password_form.is_valid():

        reset_password_form = CustomSetPasswordForm(request.user, request.POST)

              backend="django.contrib.auth.backends.ModelBackend")
        login(request, current_user,
        current_user = User.objects.get(user_id=session_user)

        session_user = request.session['auth']
    if request.method == 'POST':
            raise PermissionDenied
        if not request.session.get('auth', False):
    if request.method == 'GET':
def auth_pw_reset_view(request):
@logout_message_required
# 비밀번호찾기 새비밀번호 등록


    return HttpResponse(json.dumps({"result": user.user_id}, cls=DjangoJSONEncoder), content_type="application/json")

    request.session['auth'] = user.user_id
    user.save()
    user.auth = ""
    # login(request, user)
    user = User.objects.get(user_id=user_id, auth=input_auth_num)
    input_auth_num = request.POST.get('input_auth_num')
    user_id = request.POST.get('user_id')
    # if request.method=='POST' and 'auth_confirm' in request.POST:
def auth_confirm_view(request):


# 비밀번호찾기 인증번호 확인

    return HttpResponse(json.dumps({"result": result_pw.user_id}, cls=DjangoJSONEncoder), content_type="application/json")
    # print(auth_num)
        # print('이메일전송완료')
        )
            })
                'auth_num': auth_num,
            html_message=render_to_string('users/recovery_email.html', {
            from_email='david90907@naver.com',
            recipient_list=[email],
            '{}님의 비밀번호 찾기 인증메일입니다.'.format(user_id),
            message='',
        send_mail(
        result_pw.save()
        result_pw.auth = auth_num
        auth_num = email_auth_num()
    if result_pw:

    result_pw = User.objects.get(user_id=user_id, name=name, email=email)
    email = request.POST.get('email')
    name = request.POST.get('name')
    user_id = request.POST.get('user_id')
def ajax_find_pw_view(request):
# 비밀번호찾기 AJAX 통신
