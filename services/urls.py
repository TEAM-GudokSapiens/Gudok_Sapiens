from django.urls import path, include
from . import views

app_name = 'services'

urlpatterns = [
    path('main/', views.main, name='main'),
    path('search/',views.search, name='search' ),
    path('list/', views.services_list, name='services_list'),
    path('list/<slug:category_slug>/', views.category_list, name='category_list'),
    path('list/<slug:category_slug>/<slug:sub_category_slug>/', views.sub_category_list, name ='sub_category_list'),
    path('detail/<int:pk>/', views.services_detail, name='services_detail'),
    path('tags/', views.services_tags, name='services_tags'),
    path('same_tag_list/<str:tag>', views.same_tag_list, name='same_tag_list'),
    # path('dibs_ajax/', views.dibs_ajax, name='dibs_ajax'),
]
