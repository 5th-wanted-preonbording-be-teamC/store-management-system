from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from users import serializers
from users.models import User


class RegisterAPIView(APIView):
    def post(self, request):
        """
        회원 가입
        POST /api/v1/users/
        """
        serializer = serializers.UserRegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.create(request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        """
        회원 목록
        GET /api/v1/users/
        """
        users = User.objects.all()
        serializer = serializers.UserSerializer(users, many=True)
        return Response(serializer.data)
