from django.contrib import admin
from .models import Review
from .forms import ReviewCreateForm

# Register your models here.


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['title', 'target', 'user']
    list_display_links = ['title']
