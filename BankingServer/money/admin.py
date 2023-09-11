from django.contrib import admin
from .models import Money, Bank

class MoneyAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'account_number', 'bank_name', 'balance')

admin.site.register(Money, MoneyAdmin)

class BankAdmin(admin.ModelAdmin):
    list_display = ('id', 'bank_name')

admin.site.register(Bank, BankAdmin)