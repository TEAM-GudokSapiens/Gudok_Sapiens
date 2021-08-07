from django.contrib import admin
from .models import *

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
        list_display = (
        'target', 
        'content',
        'user',
        'created_at',
        'updated_at',
    )
search_fields = ('target', 'user_email', 'content',)

