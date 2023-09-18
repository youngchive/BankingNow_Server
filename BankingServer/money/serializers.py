from rest_framework import serializers
from .models import Money, Transfer

class TransferSerializer(serializers.ModelSerializer):
    account_bank_to = serializers.CharField(source='money.bank_name', max_length=10)
    account_no_to = serializers.CharField(max_length=20)

    class Meta:
        model = Transfer
        fields = '__all__'


class BalanceCheckSerializer(serializers.Serializer):
    balance = serializers.IntegerField()

