from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('create/', views.ReviewCreateView.as_view(),
         name='create'),
    #     path('create/<int:pk>', views.reviews_create,
    #          name='create'),
    #
]
