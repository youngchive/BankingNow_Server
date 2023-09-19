from rest_framework import serializers
from .models import Money, Transfer

class AccountCheckSerializer(serializers.Serializer):
    account_number = serializers.CharField(max_length=50)
    bank_name = serializers.CharField()


class TransferSerializer(serializers.ModelSerializer):
    account_bank_to = serializers.CharField(source='money.bank_name', max_length=10)
    account_no_to = serializers.CharField(max_length=20)

    class Meta:
        model = Transfer
        fields = '__all__'


class BalanceCheckSerializer(serializers.Serializer):
    balance = serializers.IntegerField()
    user_id = serializers.CharField()  # 사용자 ID 필드를 추가
    bank_name = serializers.CharField()  # 은행 이름 필드를 추가
