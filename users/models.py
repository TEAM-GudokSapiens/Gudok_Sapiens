from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    GENDERS = (
        ('MALE', 'MALE'),
        ('FEMALE', 'FEMALE'),
    )

    email = models.EmailField(verbose_name='email', unique=True, )
    name = models.CharField(verbose_name='name', max_length=30)
    nickname = models.CharField(verbose_name='nickname', max_length=30)
    phonenum = models.CharField(verbose_name='phonenum', max_length=30)
    gender = models.CharField(verbose_name='gender',
                              choices=GENDERS, max_length=30)
    created_at = models.DateTimeField('created_at', default=timezone.now)

    def __str__(self):
        return self.username
