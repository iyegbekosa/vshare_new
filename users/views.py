from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterUserSerializer, RegisterDriverSerializer, UserProfileSerializer
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from .helper import get_tokens_for_user
from rest_framework.permissions import IsAuthenticated


class CustomUserCreate(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        reg_serializer = RegisterUserSerializer(data=request.data)
        if reg_serializer.is_valid():
            reg_serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(reg_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class CustomDriverCreate(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegisterDriverSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Driver registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RiderLoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response({"detail": "Email and password are required."}, status=400)

        user = authenticate(request, email=email, password=password)
        if user is None or user.role != 'rider':
            return Response({"detail": "Invalid rider credentials."}, status=401)

        return Response(get_tokens_for_user(user), status=200)
    

class DriverLoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response({"detail": "Email and password are required."}, status=400)

        user = authenticate(request, email=email, password=password)
        if user is None or user.role != 'driver':
            return Response({"detail": "Invalid driver credentials."}, status=401)

        return Response(get_tokens_for_user(user), status=200)
    

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)