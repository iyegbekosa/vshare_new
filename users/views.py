from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterUserSerializer, RegisterDriverSerializer
from rest_framework.permissions import AllowAny

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
