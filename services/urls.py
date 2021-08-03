from django.urls import path, include
from . import views

app_name = 'services'

urlpatterns = [
    path('main/', views.main, name='main'),
    # path('list/', views.services_list, name='services_list'),
    path('detail/<int:pk>/', views.services_detail, name='services_detail'),
]
