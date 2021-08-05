from django.urls import path, include
from . import views

app_name = 'services'

urlpatterns = [
    path('main/', views.main, name='main'),
    # path('service_list/', views.ServiceListView.as_view(), name='service_list_view'),
    path('search/', views.search, name='search'),
    path('list/', views.services_list, name='services_list'),
    path('list/<slug:slug>/', views.category_list, name='category_list'),
    path('detail/<int:pk>/', views.services_detail, name='services_detail'),
]
