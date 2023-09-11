from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from users.models import User  # 사용자 모델의 정확한 임포트 경로로 변경

from django.contrib.auth import authenticate

from accounts.serializers import PasswordCheckSerializer


# http://localhost:8000/accounts/check_password/ 링크로 접근
class PasswordCheckView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PasswordCheckSerializer(data=request.data)
        if serializer.is_valid():
            # 비밀번호 확인 로직
            password = serializer.validated_data['password']

            # 사용자 검색
            user = User.objects.filter(user_id='capjjang').first()
            if user:
                # 사용자 인증
                print(password)
                print(user.user_id)
                user_authenticated = authenticate(username=user.user_id, password=password)
                if user_authenticated is not None:
                    return Response({'is_password_correct': True})
                else:
                    return Response({'is_password_correct': False})
            else:
                return Response({'is_password_correct': False})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
