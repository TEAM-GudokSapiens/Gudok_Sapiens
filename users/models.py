from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone


class User(AbstractBaseUser):
    GENDERS = (
        ('MALE', '남성(Man)'),
        ('FEMALE', '여성(Woman)'),
    )

    email_id = models.EmailField(verbose_name='email_id', unique=True)
    name = models.CharField(verbose_name='name', max_length=30)
    nickname = models.CharField(verbose_name='nickname', max_length=30)
    phonenum = models.CharField(verbose_name='phonenum', max_length=30)
    gender = models.CharField(verbose_name='gender',choices=GENDERS)
    created_at = models.DateTimeField('created_at', default=timezone.now)
    
    USERNAME_FIELD = 'email'                     # email을 사용자의 식별자로 설정
    REQUIRED_FIELDS = ['name']                   # 필수입력값
   
    def email_user(self, subject, message, from_email=None, **kwargs): # 이메일 발송 메소드
        send_mail(subject, message, from_email, [self.email], **kwargs)

