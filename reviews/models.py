from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator


class Review(models.Model):
    target = models.ForeignKey(
        "services.Service", related_name='review_target', on_delete=models.CASCADE, verbose_name='서비스')
    user = models.ForeignKey(
        "users.User", related_name='review_user', on_delete=models.CASCADE, verbose_name='유저'
    )
    photo = models.ImageField(
        verbose_name='리뷰사진', blank=True, null=True, upload_to='%Y/%m/%d')
    title = models.CharField(verbose_name='리뷰제목', max_length=50)
    content = models.TextField(verbose_name='내용', validators=[
        MinLengthValidator(15)])
    score = models.PositiveSmallIntegerField(verbose_name='별점', validators=[
        MinValueValidator(0), MaxValueValidator(10)])
    period = models.PositiveSmallIntegerField(verbose_name='사용기간')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)