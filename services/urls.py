from django.urls import path, include, re_path
from django.conf.urls import url
from . import views

app_name = 'services'

urlpatterns = [
    path('main/', views.main, name='main'),
    path('search/', views.search, name='search'),
    path('list/', views.services_list, name='services_list'),
    path('list/<str:category_slug>/', views.category_list, name='category_list'),
    path('list/<slug:category_slug>/<slug:sub_category_slug>/', views.sub_category_list, name='sub_category_list'),
    path('detail/<int:pk>/', views.services_detail, name='services_detail'),
    path('tags/', views.services_tags, name='services_tags'),
    path('same_tag_list/<str:tag>', views.same_tag_list, name='same_tag_list'),
    path('service_intro', views.service_intro, name='service_intro'),
    path('list/lifestyle/', views.category_lifestyle, name='category_lifestyle'),
    path('list/content/', views.category_content, name='category_content'),
    path('list/food/', views.category_food, name='category_food'),
    path('list/newsletter/', views.category_newsletter, name='category_newsletter'),
    path('list/other/', views.category_other, name='category_other'),
    path('list/lifestyle/daily-item/', views.subcategory_daily_item, name='subcategory_daily_item'),
    path('list/lifestyle/health/', views.subcategory_health, name='subcategory_health'),
    path('list/lifestyle/clothing/', views.subcategory_clothing, name='subcategory_clothing'),
    path('list/lifestyle/cleaning/', views.subcategory_cleaning, name='subcategory_cleaning'),
    path('list/food/delivery/', views.subcategory_delivery, name='subcategory_delivery'),
    path('list/food/beverage/', views.subcategory_beverage, name='subcategory_beverage'),
    path('list/food/alcohol/', views.subcategory_alcohol, name='subcategory_alcohol'),
    path('list/food/fruit/', views.subcategory_fruit, name='subcategory_fruit'),
    path('list/food/health-food/', views.subcategory_health_food, name='subcategory_health_food'),
    path('list/food/bakery/', views.subcategory_bakery, name='subcategory_bakery'),
    path('list/food/meal-kit/', views.subcategory_meal_kit, name='subcategory_meal_kit'),
    path('list/food/snack/', views.subcategory_snack, name='subcategory_snack'),
    path('list/content/video/', views.subcategory_video, name='subcategory_video'),
    path('list/content/music/', views.subcategory_music, name='subcategory_music'),
    path('list/content/book/', views.subcategory_book, name='subcategory_book'),
]
