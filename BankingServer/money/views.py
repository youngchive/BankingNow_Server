from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from users.models import User  # 사용자 모델의 정확한 임포트 경로로 변경

from django.contrib.auth import authenticate

from .serializers import BalanceCheckSerializer
from .models import Money

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
