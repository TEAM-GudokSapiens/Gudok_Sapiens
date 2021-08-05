from django.db import models
from users.models import User

class Like(models.Model):
    active=models.SmallIntegerField(verbose_name='좋아요여부', default=0)
    users = models.ManyToManyField(
        "users.User", related_name='review_likes')
    # Foregin key랑 고민중 ajax까지 해보고 최종 결정
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
