from django.contrib import admin
from .models import MyUser
from django.contrib.auth.admin import UserAdmin

class MyUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'date_joined', 'is_admin', 'is_staff')
    search_fields = ('email', 'username')
    readonly_fields = ('id', 'date_joined', 'last_login') #authomatically changed by the system
    filter_horizontal = []
    list_filter = []
    fieldsets = []
    
admin.site.register(MyUser, MyUserAdmin)