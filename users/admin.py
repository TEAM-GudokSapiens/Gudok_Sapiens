
from django.contrib import admin
from .models import User
from django.contrib.auth.models import Group

# Register your models here.


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    fields = ('user_id', 'email', 'name', 'phonenum', 'image',
              'gender', 'level', 'is_active')
    list_display = (
        'user_id',
        'name',
        'level',
    )
    search_fields = ('user_id', 'name', 'email')


# class UserAdmin(admin.ModelAdmin):
#     fields = ('user_id', 'email', 'name', 'phonenum', 'gender', 'level',)
#     list_display = (
#         'user_id',
#         'name',
#         'level',
#         )
#     search_fields = ('user_id', 'name', 'email')

# admin.site.register(User, UserAdmin)
# admin.site.unregister(Group) # Admin페이지의 GROUP삭제
