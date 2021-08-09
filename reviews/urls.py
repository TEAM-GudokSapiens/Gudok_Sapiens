from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('create/<int:pk>', views.reviews_create, name='create'),
    path('submit_ajax/<int:pk>', views.submit_ajax, name='submit_ajax')
]
