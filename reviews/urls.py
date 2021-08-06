from django.urls import path, include
from . import views

app_name = 'reviews'

urlpatterns = [
    path('submit_ajax/', views.submit_ajax, name='submit_ajax')
]
