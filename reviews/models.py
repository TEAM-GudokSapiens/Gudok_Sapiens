from django.db import models
from services.models import Service
from users.models import User
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator


class Review(models.Model):
    target_service = models.ForeignKey(
        Service, on_delete=models.CASCADE, verbose_name='서비스')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='유저')
    title = models.CharField(verbose_name='리뷰제목', max_length=50)
    content = models.TextField(verbose_name='리뷰내용', validators=[
        MinLengthValidator(150)])
    photo = models.ImageField(
        verbose_name='리뷰사진', blank=True, upload_to='%Y/%m/%d')
    score = models.PositiveSmallIntegerField(verbose_name='별점', validators=[
        MinValueValidator(0), MaxValueValidator(10)])
    period = models.PositiveSmallIntegerField(verbose_name='사용기간')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_total_likes(self):
        return self.likes.users.count()


class Like(models.Model):

    review = models.OneToOneField(
        Review, related_name="likes", on_delete=models.CASCADE)
    users = models.ManyToManyField(
        User, related_name='requirement_review_likes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.review.content)[:30]
