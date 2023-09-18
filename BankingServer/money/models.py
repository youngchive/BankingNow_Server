from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError  # ValidationError 임포트 추가
from django.contrib.auth.models import User  # User 모델 임포트 추가

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
    money = models.ForeignKey(Money, on_delete=models.CASCADE, related_name='transfers_as_money')
    # user_to 필드를 Money 모델과 연결된 사용자와 연결
    user_to = models.ForeignKey(Money, on_delete=models.CASCADE, verbose_name='받는 사람', related_name='transfers_as_user_to')
    
    account_no_to = models.CharField(max_length=20, verbose_name='받는 계좌번호')
    #account_no_from = models.CharField(max_length=20, verbose_name='주는 계좌번호')

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
    #account_bank_from = models.CharField(max_length=10, verbose_name='주는 은행', choices=bank_list)

    amount = models.DecimalField(
        decimal_places=0,
        max_digits=10,
        verbose_name='금액',
        validators=[
            MinValueValidator(Decimal('10'))
        ]
    )
    #timestamp   = models.DateTimeField(auto_now_add=True)
    action_name = 'Transfer'

    def get_action_name(self):
        return self.action_name 

    def set_action_name(self, action_name):
        self.action_name = action_name
        return action_name

    # def __str__(self):
    #     return str(self.id)
    
    def save(self, *args, **kwargs):
        # 이체를 수행하려는 사용자 정보 가져오기
        money_user = get_money_user(self.user_to.user_id)
        if money_user:
            # Money 모델에 있는 사용자와 일치하는 경우에만 이체를 저장
            super(Transfer, self).save(*args, **kwargs)
        else:
            # Money 모델에 있는 사용자와 일치하지 않는 경우 이체 거부
            raise ValidationError("이체를 수행할 수 없는 사용자입니다.")
        
# Money 모델에 있는 사용자 정보를 가져오기 위한 함수
def get_money_user(user_id):
    try:
        return Money.objects.get(user_id=user_id)
    except Money.DoesNotExist:
        return None