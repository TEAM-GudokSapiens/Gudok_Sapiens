from django.urls import path
from django.conf import settings
from django.conf.urls import url
from django.urls.conf import path
from django.urls.resolvers import URLPattern
from . import views

from django.conf.urls.static import static

app_name = 'users'

urlpatterns = [
    path('signup/', views.signup, name='signup'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)