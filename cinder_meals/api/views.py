from django.shortcuts import render
from django.contrib.auth import authenticate, logout
from rest_framework import generics,permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView

from accounts.models import User
from dashboard.models import Order, Delivery, Payment,Meal, OrderItem, Banner, Restaurant
from cinder_meals.utils.constants import *

from api.serializers import UserSerializer, RegisterSerializer, LoginSerializer, RestaurantSerializer, BannerSerializer, MealSerializer, OrderSerializer

class UsersAPI(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]

class RegisterAPI(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        error_message = ""
        request_data = request.data.copy()
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            for field in list(e.detail):
                error_message = e.detail[field][0]
                response_data = {
                    "error_message" : error_message,
                    "user" : None,
                    "token" : None,
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        user = serializer.save()
        
        response_data = {
            "error_message" : None,
            "user" : UserSerializer(user, context=self.get_serializer_context()).data,
            "token" : AuthToken.objects.create(user)[1],
        }
        return Response(response_data, status=status.HTTP_200_OK)
        

class LoginAPI(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            for field in list(e.detail):
                error_message = e.detail[field][0]
                response_data = {
                    "error_message" : error_message,
                    "user" : None,
                    "token" : None,
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        user = serializer.validated_data
        user.save()
        
        response_data = {
            "error_message" : None,
            "user" : UserSerializer(user, context=self.get_serializer_context()).data,
            "token" : AuthToken.objects.create(user)[1],
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
        
class LogoutAPI(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)
    