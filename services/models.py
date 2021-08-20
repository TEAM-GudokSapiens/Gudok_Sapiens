from django.db import models
from users.models import User
from taggit.managers import TaggableManager
from django.core.paginator import Paginator
from django.db.models import Count, Avg


class Category(models.Model):
    name = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=150, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def get_services_by_category(self):
        return Service.objects.annotate(
        num_dibs=Count('dib')).annotate(avg_reviews=Avg('review__score')).order_by('-num_dibs').filter(category__name=self.name)

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
    tags = TaggableManager(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_review(self):
        reviews = self.review.all()
        return reviews

    def get_review_count(self):
        counts = self.review.all().count()
        return counts