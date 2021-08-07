from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, user_id, email, password, name, nickname, phonenum, gender, created_at, **extra_fields):
        user = self.model(
            user_id=user_id,
            email=email,
            name=name,
            nickname=nickname,
            phonenum=phonenum,
            gender=gender,
            created_at=created_at,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_id,  password, email=None, name=None, nickname=None, phonenum=None, gender=None):
        user = self.create_user(user_id, email, password, email,
                                name, nickname, phonenum, gender)
        user.is_superuser = True
        user.is_staff = True
        user.is_admin = True
        user.level = 0
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()

    GENDERS = (
        ('MALE', 'MALE'),
        ('FEMALE', 'FEMALE'),
    )
    LEVEL_CHOICES = (
        ("3", "Lv3_미인증사용자"),
        ("2", "Lv2_인증사용자"),
        ("1", "Lv1_관리자"),
        ("0", "Lv0_개발자"),
    )
    user_id = models.CharField(
        verbose_name='아이디', max_length=30, unique=True)
    email = models.EmailField(verbose_name='email', null=True, unique=True)
    password = models.CharField(max_length=256, verbose_name="비밀번호")
    name = models.CharField(verbose_name='name', max_length=30, null=True)
    nickname = models.CharField(
        verbose_name='nickname', max_length=30, null=True)
    phonenum = models.CharField(
        verbose_name='phonenum', max_length=30, null=True)
    gender = models.CharField(verbose_name='gender',
                              choices=GENDERS, max_length=30, null=True)
    level = models.CharField(choices=LEVEL_CHOICES,
                             max_length=18, verbose_name="등급", default=3)
    created_at = models.DateTimeField(
        'created_at', default=timezone.now, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'user_id'

    def __str__(self):
        return self.username
