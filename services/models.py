from django.db import models
from likes.models import Like
class Category(models.Model):
    name = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=150, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-created_at', )
        verbose_name = 'category'
        verbose_name_plural = 'categories'


class SubCategory(models.Model):
    category = models.ForeignKey(
        Category, related_name='sub_category', on_delete=models.CASCADE)
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
    img1 = models.ImageField(verbose_name='사진',
                             blank=True, upload_to="%Y/%m/%d")
    img2 = models.ImageField(verbose_name='사진2',
                             blank=True, upload_to="%Y/%m/%d")
    img3 = models.ImageField(verbose_name='사진3',
                             blank=True, upload_to="%Y/%m/%d")
    img4 = models.ImageField(verbose_name='사진4',
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
    # dibs = models.OneToOneField(
    #     Like, on_delete=models.PROTECT, verbose_name='찜',blank=True,null=True)

    # def get_total_dibs(self):
    #     return self.dibs.users.count()


# class Dib(models.Model):
#     service = models.OneToOneField(
#         Service, related_name="dibs", on_delete=models.CASCADE)
#     users = models.ManyToManyField(
#         User, related_name='requirement_service_dibs')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)


class Tag(models.Model):
    service = models.ManyToManyField(
        Service, related_name='tags')
