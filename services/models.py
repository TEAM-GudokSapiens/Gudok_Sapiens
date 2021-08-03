from django.db import models
from users.models import User


# CATEGORY = {
#     ('라이스프타일', '라이프스타일'),
#     ('음식', '음식'),
#     ('컨텐츠', '컨텐츠'),
#     ('뉴스레터', '뉴스레터'),
# }

# LIFESTYLE_CATEGORY = {
#     ('생활', '생활'),
#     ('건강/헬스', '건강/헬스,'),
#     ('의류', '의류'),
#     ('청소', '청소'),
#     ('애완동물', '애완동물'),
# }

# FOOD_CATEGORY = {
#     ('홈배달', '홈배달'),
#     ('음료', '음료'),
#     ('샐러드', '샐러드'),
#     ('과일/야채', '과일/야채'),
#     ('건강식품', '건강식품'),
#     ('주류', '주류'),
#     ('베이커리', '베이커리'),
#     ('패스트푸드', '패스트푸드'),
# }

# CONTENTS_CATEGORY = {
#     ('영상', '영상'),
#     ('음악', '음악'),
#     ('도서', '도서'),
# }

# NEWS_CATEGORY = {
# }

class Category(models.Model):
    name = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=150, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nameW

    class Meta:
        ordering = ('-created_at', )
        verbose_name = 'category'
        verbose_name_plural = 'categories'


class SubCategory(models.Model):
    category = models.ForeignKey(
        Category, related_name='souscatégories', on_delete=models.CASCADE)
    name = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=150, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at', )
        verbose_name = 'sub-category'
        verbose_name_plural = 'sub-categories'

    def __str__(self):
        return self.name


class Service(models.Model):
    img = models.ImageField(verbose_name='대표사진',
                            blank=True, upload_to="%Y/%m/%d")
    name = models.CharField(verbose_name='서비스 명', max_length=30)
    intro = models.CharField(verbose_name='한줄 소개', max_length=30)
    content = models.TextField(verbose_name='서비스 내용')
    category = models.ForeignKey(
        Category, related_name='services', on_delete=models.CASCADE)
    subcategory = models.ForeignKey(
        SubCategory, related_name='services', on_delete=models.CASCADE)
    price = models.IntegerField(verbose_name='최저 가격')
    link = models.URLField(verbose_name='서비스 홈페이지', max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_total_dibs(self):
        return self.dibs.users.count()


class Dib(models.Model):
    service = models.OneToOneField(
        Service, related_name="dibs", on_delete=models.CASCADE)
    users = models.ManyToManyField(
        User, related_name='requirement_service_dibs')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Tag(models.Model):
    service = models.ManyToManyField(
        Service, related_name='tags')
