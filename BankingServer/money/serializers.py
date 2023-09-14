from rest_framework import serializers
from .models import Money, Transfer

class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = '__all__'