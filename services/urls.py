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
    # path('list/<str:category>/', views.category_list_str, name='category_list_str'),
    # url(r'^list/(?P<category>[-\w]+)/$', views.category_list_str, name='category_list_str'),
    # path('list/lifestyle/', views.category_list, name='category_lifestyle'),
    # path('list/food/', views.category_list, name='category_food'),
    # path('list/newsletter/', views.category_list, name='category_newsletter'),
    # path('list/other/', views.category_list, name='category_other'),
]
