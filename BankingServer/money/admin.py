from django.contrib import admin
from .models import Money, Bank, Transfer

class MoneyAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'account_number', 'display_bank_name', 'balance')

    def display_bank_name(self, obj):
        if obj.bank_name:
            return obj.bank_name.bank_name
        else:
            return "No Bank"

    display_bank_name.short_description = "받는 은행"  # 컬럼 헤더 이름 설정

admin.site.register(Money, MoneyAdmin)

class BankAdmin(admin.ModelAdmin):
    list_display = ('id', 'bank_name')

admin.site.register(Bank, BankAdmin)

class TransferAdmin(admin.ModelAdmin):
    list_display = ('id', 'account_no_to', 'account_bank_to', 'user_to', 'amount')

admin.site.register(Transfer, TransferAdmin)