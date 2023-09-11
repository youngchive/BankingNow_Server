from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Money(models.Model):
    user_id = models.TextField(verbose_name='이름')
    account_number = models.CharField(max_length=50, verbose_name='계좌번호', blank=True, null=True)
    bank_name = models.ForeignKey('Bank', verbose_name='은행', on_delete=models.CASCADE, blank=True, null=True, default='')
    balance = models.IntegerField(verbose_name='잔액', default=0)

    def __str__(self):
        if self.bank_name:
            return self.bank_name.bank_name  # 외래 키로 연결된 Bank 모델의 bank_name 필드 값 반환
        else:
            return "No Bank"  # 은행이 지정되지 않은 경우

class Bank(models.Model):
    bank_name = models.CharField(max_length=20, verbose_name='은행', blank=True, null=True, default='')
