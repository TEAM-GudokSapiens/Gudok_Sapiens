from django.contrib import admin
from .models import Dib

@admin.register(Dib)
class DibAdmin(admin.ModelAdmin):
    pass