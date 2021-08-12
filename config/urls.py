from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from ckeditor_uploader import views as views_ckeditor
from django.views.decorators.cache import never_cache

urlpatterns = [
    path('', lambda req: redirect('services:services_list'), name='root'),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('services/', include('services.urls', namespace="services")),
    path('reviews/', include('reviews.urls', namespace="reviews")),
    path('accounts/', include('allauth.urls')),
    path('community/', include('community.urls')),
    path('likes/', include('likes.urls')),
        
    path('upload/', login_required(views_ckeditor.upload), name='ckeditor_upload'),
    path('browse/', never_cache(login_required(views_ckeditor.browse)), name='ckeditor_browse'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
