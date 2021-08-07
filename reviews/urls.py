from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    # path('create/', views.review_create, name='create')
    path('create/', views.ReviewCreateView.as_view(), name='create')
    # path('submit_ajax/', views.submit_ajax, name='submit_ajax')
]
