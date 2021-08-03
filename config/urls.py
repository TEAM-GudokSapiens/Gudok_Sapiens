from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls.conf import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('service/', include('services.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
