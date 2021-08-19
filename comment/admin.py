from django.contrib import admin
from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'target',
        'content',
        'user',
        'created_at',
        'deleted',
    )


search_fields = ('target__title', 'user__email', 'content',)
