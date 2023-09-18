
from django.shortcuts import render
from .models import Money, Bank, Transfer
from .serializers import TransferSerializer, BalanceCheckSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import User  # 사용자 모델의 정확한 임포트 경로로 변경

from django.contrib.auth import authenticate


class TransferView(generics.CreateAPIView):
    def post(self, request):
        serializer = TransferSerializer(data=request.data)

        if serializer.is_valid():
            # 이체 정보 저장
            transfer_instance = serializer.save()

            # 특정 사용자를 보내는 사람으로 설정 (예: user_id=1인 사용자)
            transfer_instance.money = Money.objects.get(pk=1)  # 사용자를 찾을 적절한 방법을 사용
            transfer_instance.save()

            # 계좌에서 이체 금액 차감
            money = transfer_instance.money
            amount = transfer_instance.amount

            if money.balance < amount:
                # 잔액 부족 예외 처리
                return Response({"error": "잔액 부족"}, status=status.HTTP_400_BAD_REQUEST)

            money.balance -= amount
            money.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BalanceCheckView(APIView):
    def get(self, request):
        try:
            money_instance = Money.objects.first()  # 첫번째
            balance_value = money_instance.balance
        except Money.DoesNotExist:
            # 데이터가 없을 경우 기본값 설정
            balance_value = 0

        print(money_instance.user_id)

        # 시리얼라이즈
        serializer = BalanceCheckSerializer({'balance': balance_value})

        # 시리얼라이즈된 데이터를 JSON 형식으로 반환
        return Response(serializer.data, status=status.HTTP_200_OK)
