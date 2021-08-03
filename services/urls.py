from django.urls import path, include
from . import views

app_name = 'services'

urlpatterns = [
    path('list/', views.services_list, name='services_list'),
]