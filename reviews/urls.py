from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('review_create/<int:pk>', views.review_create, name='review_create')
]
