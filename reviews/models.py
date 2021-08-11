from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator


class Review(models.Model):
    target = models.ForeignKey(
        "services.Service", related_name='review', on_delete=models.CASCADE, verbose_name='서비스')
    user = models.ForeignKey(
        "users.User", related_name='review', on_delete=models.CASCADE, verbose_name='유저'
    )
    photo = models.ImageField(
        verbose_name='인증사진', blank=True, null=True, upload_to='%Y/%m/%d')
    title = models.CharField(verbose_name='리뷰제목', max_length=50)
    content = models.TextField(verbose_name='내용', validators=[
        MinLengthValidator(15)])
    score = models.DecimalField(verbose_name='별점', max_digits=2, decimal_places=1)
    period = models.PositiveSmallIntegerField(verbose_name='사용기간(개월)')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']
    updated_at = models.DateTimeField(auto_now=True)
