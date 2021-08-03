
from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email_id', 'name', 'nickname',
                    'phonenum', 'gender', 'created_at')
