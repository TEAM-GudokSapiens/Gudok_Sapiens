from django.urls import path, include
from . import views

from django.conf import settings
from django.conf.urls.static import static

app_name = 'community'

urlpatterns = [
    path('notice/', views.notice, name='notice'),
    path('notice/<int:pk>/detail/', views.notice_detail, name='notice_detail'),

    path('magazine/', views.magazine, name='magazine'),
    path('magazine/<int:pk>/detail/', views.magazine_detail, name='magazine_detail'),

    path('board/', views.board, name='board'),
    path('board/create/', views.board_create, name='board_create'),
    path('board/<int:pk>/detail/', views.board_detail, name='board_detail'),
    path('board/<int:pk>/delete/',views.board_delete,name='board_delete'),

    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

