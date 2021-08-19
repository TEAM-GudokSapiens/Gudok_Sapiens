from django.contrib import admin
from .models import *

@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title','created_at','updated_at')
@admin.register(Magazine)
class MagazineAdmin(admin.ModelAdmin):
    pass
@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    pass

