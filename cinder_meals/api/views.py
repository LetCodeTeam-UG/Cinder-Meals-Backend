import base64
import os
from django.conf import settings
from rest_framework import generics,permissions, status
from django.contrib.auth import logout
from rest_framework.permissions import IsAuthenticated
from knox.auth import TokenAuthentication
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from knox.views import LogoutView as KnoxLogoutView
from django.views.decorators.csrf import csrf_exempt

from accounts.models import User
from dashboard.models import Order, Delivery, Payment,Meal, OrderItem, DeliveryLocation
from cinder_meals.utils.constants import *
from api.serializers import UserSerializer, RegisterSerializer, LoginSerializer,MealSerializer, OrderSerializer,OrderItemSerializer

class GetUserByIdAPI(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [
        IsAuthenticated,
    ]

class RegisterAPI(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        error_message = ""
        request_data = request.data.copy()
        serializer = self.get_serializer(data=request_data)
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
        user = serializer.save(is_customer = True)
        
        response_data = {
            "error_message" : None,
            "user" : UserSerializer(user, context=self.get_serializer_context()).data,
            "token" : AuthToken.objects.create(user)[1],
        }
        return Response(response_data, status=status.HTTP_200_OK)
        

class LoginAPI(KnoxLoginView):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer
    
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
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
        token = AuthToken.objects.create(user=user)
        
        response_data = {
            "error_message" : None,
            "user" : UserSerializer(user, context=self.serializer_class()).data,
            "token" : token[1],
        }
        response = Response(response_data, status=status.HTTP_200_OK)
        response["Authorization"] = f"Token {token[1]}"
        return response
        # return Response(response_data, status=status.HTTP_200_OK)

        
class LogoutAPI(KnoxLogoutView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        """
        Logout the user and delete the token.
        """
        # Logout the user
        logout(request)

        # Delete the token
        if request.auth is not None:
            request.auth.delete()

        # Return success response
        return Response({"success": "Successfully logged out."}, status=status.HTTP_200_OK)


class MealListAPI(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self,request):
        # Retrieve all published meals, sorted by created_at
        meals = Meal.objects.filter(published=True).order_by('-created_at')
        
        try:
            # Serialize the meals data into JSON format
            meals_data = MealSerializer(meals, many=True, context={'request': request}).data
            # Update each meal's image field to include the URL of the image file
            # for meal in meals_data:
            #     meal['image'] = request.build_absolute_uri(meal['image'])
        except Exception as e:
            # If there's an error in serialization, return an error response
            for field in list(e.detail):
                error_message = e.detail[field][0]
                response_data = {
                    "error_message" : error_message,
                    "meals" : None,
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
        # Return the serialized meals data in a success response
        response_data = {
            "error_message" : None,
            "meals" : meals_data,
        }
        return Response(response_data, status=status.HTTP_200_OK)


class MyCartAPI(generics.CreateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderItemSerializer

    def post(self, request, *args, **kwargs):
        meal_id = request.data.get('meal_id', None)
        quantity = request.data.get('quantity', 1)
        allergies = request.data.get('allergies', None)
        additional_info = request.data.get('additional_info', None)

        # Validate meal
        if not meal_id:
            return Response({'error': 'Meal is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            meal = Meal.objects.get(pk=meal_id)
        except Meal.DoesNotExist:
            return Response({'error': 'Meal does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if order item already exists for the user and meal
        order_item = OrderItem.objects.filter(user=request.user, meal=meal).first()

        if order_item:
            # Update quantity of existing order item
            order_item.quantity += quantity
            order_item.save()
        else:
            # Create new order item
            order_item = OrderItem.objects.create(user=request.user, meal=meal, quantity=quantity, allergies=allergies, additional_info=additional_info)

        return Response({'order_item_id': order_item.id}, status=status.HTTP_201_CREATED)

class OrderAPI(generics.ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user=user).order_by('-created_at')

    def post(self, request, *args, **kwargs):
        order_items_data = request.data.get('order_items', [])
        location_id = request.data.get('location', None)
        payment_method = request.data.get('payment_method', PaymentMethod.CASH.value)
        phone = request.data.get('phone', None)

        # Validate location
        if not location_id:
            return Response({'error': 'Location is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            location = DeliveryLocation.objects.get(pk=location_id)
        except DeliveryLocation.DoesNotExist:
            return Response({'error': 'Location does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create order
        order = Order.objects.create(user=request.user, location=location, payment_method=payment_method, phone=phone)

        # Add order items
        for item_data in order_items_data:
            meal_id = item_data.get('meal', None)
            quantity = item_data.get('quantity', 1)
            allergies = item_data.get('allergies', None)
            additional_info = item_data.get('additional_info', None)

            # Validate meal
            if not meal_id:
                return Response({'error': 'Meal is required.'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                meal = Meal.objects.get(id=meal_id)
            except Meal.DoesNotExist:
                return Response({'error': 'Meal does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

            # Check if order item already exists
            order_item = OrderItem.objects.filter(order=order, meal=meal).first()

            if order_item:
                # Update quantity and total price of existing order item
                order_item.quantity += quantity
                order_item.total_price = order_item.quantity * meal.price
                order_item.save()
            else:
                # Create new order item with total price
                total_price = quantity * meal.price
                order_item = OrderItem.objects.create(user=request.user, meal=meal, quantity=quantity, allergies=allergies, additional_info=additional_info, total=total_price)
                # Add order item to order
                order.order_items.add(order_item)

        # Calculate order totals
        order.sub_total =  sum(item.meal.price * item.quantity for item in order.order_items.all())
        
        order.total = order.sub_total + order.location.delivery_fee

        # Save order
        order.save()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


