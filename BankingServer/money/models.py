from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

from decimal import Decimal

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

class Transfer(models.Model):
    money = models.ForeignKey(Money, on_delete=models.CASCADE)
    account_no_to = models.CharField(max_length=20, verbose_name='받는 계좌번호')
    account_no_from = models.CharField(max_length=20, verbose_name='주는 계좌번호')

    bank_list = (
        ('국민', '국민은행'),
        ('신한', '신한은행'),
        ('우리', '우리은행'),
        ('하나', '하나은행'),
        ('농협', '농협은행'),
        ('기업', '기업은행'),
        ('토스', '토스뱅크'),
        ('카카오', '카카오뱅크'),
    )

    account_bank_to = models.CharField(max_length=10, verbose_name='받는 은행', choices=bank_list)
    account_bank_from = models.CharField(max_length=10, verbose_name='주는 은행', choices=bank_list)

    user_to = models.CharField(max_length=20, verbose_name='받는 사람')

    amount = models.DecimalField(
        decimal_places=0,
        max_digits=10,
        verbose_name='금액',
        validators=[
            MinValueValidator(Decimal('10'))
        ]
    )
    timestamp   = models.DateTimeField(auto_now_add=True)
    action_name = 'Transfer'

    def get_action_name(self):
        return self.action_name 

    def set_action_name(self, action_name):
        self.action_name = action_name
        return action_name

    def __str__(self):
        return str(self.id)