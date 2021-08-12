from django.http.response import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.forms.utils import ErrorList
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from .models import User
from django.views.generic import UpdateView, DeleteView
from users.forms import UpdateForm, LoginForm, SignupForm
from django.contrib.auth import login, logout, authenticate
from django.utils.decorators import method_decorator
from django.views.generic import FormView
from .decorators import *
from services.models import Service
from django.core.paginator import Paginator
from django.urls import reverse
from .mailing import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import PermissionDenied
from django.core.exceptions import ValidationError
from django.core.exceptions import PermissionDenied
from django.views.generic import CreateView
from django.http import HttpResponseRedirect, Http404
# 회원가입


class Signup(CreateView):
    model = User
    template_name = 'users/signup.html'
    form_class = SignupForm

    def get(self, request, *args, **kwargs):
        # if not request.session.get('agreement', False):
        #     raise PermissionDenied
        # request.session['agreement'] = False
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        # messages.success(self.request, "회원가입 성공.")
        self.request.session['register_auth'] = True
        messages.success(
            self.request, '회원님의 입력한 Email 주소로 인증 메일이 발송되었습니다. 인증 후 로그인이 가능합니다.')
        # return settings.LOGIN_URL
        return reverse('users:register_success')

    def form_valid(self, form):
        self.object = form.save()

        # 회원가입 인증 메일 발송
        # ISSUE - https 통신오류 -> http 프로토콜 수정
        send_mail(
            '[구독사피엔스] {}님의 회원가입 인증메일 입니다.'.format(self.object.user_id),
            [self.object.email],
            html=render_to_string('users/register_email.html', {
                'user': self.object,
                'uid': urlsafe_base64_encode(force_bytes(self.object.pk)).encode().decode(),
                'domain': self.request.META['HTTP_HOST'],
                'token': default_token_generator.make_token(self.object),
            }),
        )
        return redirect(self.get_success_url())

# def signup(request):
#     if request.method == "POST":
#         form = SignupForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             user_id = form.cleaned_data.get('user_id')
#             raw_password = form.cleaned_data.get('password1')
#             user = authenticate(username=user_id, password=raw_password)
#             send_mail('[] {}님의 회원가입 인증메일 입니다.'.format(user_id), [user.email], html=render_to_string('users/register_email.html', {
#                 'user': user_id,
#                 'uid': urlsafe_base64_encode(force_bytes(user.pk)).encode().decode(),
#                 'domain': user.request.META['HTTP_HOST'],
#                 'token': default_token_generator.make_token(user_id),
#             }))
#             return redirect(user.get_success_url())

#     else:
#         form = SignupForm()
#     ctx = {'form': form}
#     return render(request, template_name="users/signup.html", context=ctx)


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
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist, ValidationError):
        messages.error(request, '메일 인증에 실패했습니다.')
        return redirect('users:login')

    if default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.info(request, '메일 인증이 완료 되었습니다. 회원가입을 축하드립니다!')
        return redirect('users:login')
        # form = SignupForm(request.POST)
        # user = form.save()
        # user_id = form.cleaned_data.get('user_id')
        # raw_password = form.cleaned_data.get('password1')
        # user = authenticate(username=user_id, password=raw_password)
        # login(request, user)
        # return redirect('services:main')

    messages.error(request, '메일 인증에 실패했습니다.')
    return redirect('users:login')

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

# 회원탈퇴


class AccountDeleteView(DeleteView):
    model = User
    success_url = reverse_lazy('users:login')
    template_name = 'users/delete.html'

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
    reviews_list = Service.objects.filter(
        review__user=request.user.id).distinct()
    # 한 페이지 당 담을 수 있는 객체 수를 정할 수 있음
    paginator = Paginator(reviews_list, 10)
    page = request.GET.get('page')
    services = paginator.get_page(page)

    ctx = {
        'services': services,
    }
    return render(request, 'users/dibs_list.html', context=ctx)
