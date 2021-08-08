from django.urls import path
from . import views

app_name = 'likes'

urlpatterns = [
    path('dibs/<int:pk>', views.likes_dibs, name='likes_dibs'),
    path('helps/<int:pk>', views.likes_helps, name='likes_helps'),
]