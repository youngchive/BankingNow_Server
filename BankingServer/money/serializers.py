from rest_framework import serializers

class BalanceCheckSerializer(serializers.Serializer):
    balance = serializers.IntegerField()
