from django.db import models
from services.models import Category
from users.models import User
from comment.models import Comment


class Notice(models.Model):
    title = models.CharField(verbose_name='제목', max_length=30)
    content = models.TextField(verbose_name='서비스 내용')
    img = models.ImageField(verbose_name='사진',
                            blank=True, upload_to="%Y/%m/%d")
    hits = models.PositiveIntegerField(verbose_name='조회수', default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Magazine(models.Model):    
    category = models.ForeignKey(
        Category, related_name='magazine', on_delete=models.PROTECT,blank=True,null=True)
    title = models.CharField(verbose_name='제목', max_length=30)    
    intro = models.CharField(verbose_name='한줄 소개', max_length=30)
    content = models.TextField(verbose_name='서비스 내용')
    img = models.ImageField(verbose_name='사진',
                            blank=True, upload_to="%Y/%m/%d")
    hits = models.PositiveIntegerField(verbose_name='조회수', default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Board(models.Model):
    user = models.ForeignKey(User, related_name='board',
                             on_delete=models.CASCADE)
    title = models.CharField(verbose_name='제목', max_length=30)
    content = models.TextField(verbose_name='서비스 내용')
    img = models.ImageField(verbose_name='사진',
                            blank=True, upload_to="%Y/%m/%d")
    hits = models.PositiveIntegerField(verbose_name='조회수', default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
