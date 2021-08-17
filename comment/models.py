from django.db import models
from django.apps import apps
from django.core.validators import MinLengthValidator
from datetime import datetime, timedelta
from django.utils import timezone


class Comment(models.Model):
    target = models.ForeignKey(
        "community.Board", related_name='comment', on_delete=models.CASCADE, verbose_name='게시글')
    user = models.ForeignKey(
        "users.User", related_name='comment', on_delete=models.CASCADE, verbose_name='유저'
    )
    content = models.TextField(verbose_name='내용', validators=[
        MinLengthValidator(15)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False, verbose_name='삭제여부')
    reply = models.IntegerField(verbose_name='답글위치', default=0)

    def __str__(self):
        return self.content

    @property
    def created_string(self):
        time = datetime.now(tz=timezone.utc) - self.created_at

        if time < timedelta(minutes=1):
            return '방금 전'
        elif time < timedelta(hours=1):
            return str(int(time.seconds / 60)) + '분 전'
        elif time < timedelta(days=1):
            return str(int(time.seconds / 3600)) + '시간 전'
        elif time < timedelta(days=7):
            time = datetime.now(tz=timezone.utc).date() - \
                self.created_at.date()
            return str(time.days) + '일 전'
        else:
            return False

    class Meta:
        db_table = '자유게시판 댓글'
        verbose_name = '자유게시판 댓글'
        verbose_name_plural = '자유게시판 댓글'
