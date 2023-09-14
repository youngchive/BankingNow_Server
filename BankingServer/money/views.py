from django.shortcuts import render
from .models import Money, Bank, Transfer
from .serializers import TransferSerializer
from rest_framework import generics

# 교직원 회원가입
class TransferView(generics.CreateAPIView):
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer
