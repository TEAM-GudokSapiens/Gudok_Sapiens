from django.contrib import admin
from .models import Service, Category


@admin.register(Category)
class IdeaAdmin(admin.ModelAdmin):
    pass 
@admin.register(Service)
class IdeaAdmin(admin.ModelAdmin):
    pass 

