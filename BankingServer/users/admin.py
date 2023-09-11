from django.contrib import admin
from .models import User

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'user_id', 'password')
    fields = ('name', 'user_id', 'password')

admin.site.register(User, UserAdmin) # 사용자 안에서 약/영양제 확인 가능
