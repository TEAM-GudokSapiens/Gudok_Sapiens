from django.urls import path, include
from . import views

from django.conf import settings
from django.conf.urls.static import static

app_name = 'community'

urlpatterns = [
    path('notice/', views.notice, name='notice'),
    path('notice/<int:pk>/detail/', views.notice_detail, name='notice_detail'),

    path('magazine/', views.magazine, name='magazine'),
    path('magazine/<int:pk>/detail/',
         views.magazine_detail, name='magazine_detail'),

    path('board/', views.board, name='board'),
    path('board/create/', views.board_create, name='board_create'),
    path('board/<int:pk>/detail/', views.board_detail, name='board_detail'),
    path('board/<int:pk>/delete/', views.board_delete, name='board_delete'),
    path('board/<int:pk>/update/', views.board_update, name='board_update'),
    path('board/like/', views.likes, name="likes"),

    path('comment/<int:pk>/write/', views.comment_write, name='comment_write'),
    path('comment/<int:pk>/delete/',
         views.comment_delete, name='comment_delete'),

    path('search/', views.search, name='search'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
