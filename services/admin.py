from django.contrib import admin
from .models import Service, Category, SubCategory
<<<<<<< HEAD


@admin.register(Category)
class IdeaAdmin(admin.ModelAdmin):
    pass 

@admin.register(SubCategory)
class IdeaAdmin(admin.ModelAdmin):
    pass 
@admin.register(Service)
class IdeaAdmin(admin.ModelAdmin):
    pass 

=======


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    pass
>>>>>>> 0d1a5b323888b404fb0fbd3f9a85b7c455b0649f
