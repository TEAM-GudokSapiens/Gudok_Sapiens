from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect


urlpatterns = [
    path('', lambda req: redirect('services:services_list'), name='root'),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('services/', include('services.urls', namespace="services")),
    path('reviews/', include('reviews.urls', namespace="reviews")),
    path('accounts/', include('allauth.urls')),
    path('community/', include('community.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
