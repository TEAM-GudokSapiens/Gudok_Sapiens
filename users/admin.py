
from django.contrib import admin

from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email_id', 'name', 'nickname', 'phonenum', 'gender','created_at')
    list_display_links = ('email_id', 'name',)
    exclude = ('password',)                        

    def joined_at(self, obj):
        return obj.date_joined.strftime("%Y-%m-%d")

    joined_at.admin_order_field = '-date_joined'      
    joined_at.short_description = '가입일'
