from django.shortcuts import get_object_or_404
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

class UserDetailAPIView(APIView):
    def get_object(self, pk):
        return get_object_or_404(User, pk=pk)

    def get(self, request, pk):
        """
        회원 상세
        GET /api/v1/users/{pk}
        """
        user = self.get_object(pk=pk)
        serializer = serializers.UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        """
        회원 정보 수정
        PUT /api/v1/users/{pk}
        """
        user = self.get_object(pk=pk)
        serializer = serializers.UserUpdateSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)