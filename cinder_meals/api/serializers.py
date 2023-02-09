from rest_framework import serializers
from accounts.models import User
from dashboard.models import Order, Delivery, Payment,Meal, OrderItem, Banner, Restaurant
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'fullname', 'username', 'gender', 'phone')

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'fullname','gender', 'phone', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'address', 'phone')

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ('id', 'title', 'image')

class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = ('id', 'title', 'type', 'description', 'price', 'image')

class OrderSerializer(serializers.ModelSerializer):
    payment_status = serializers.SerializerMethodField("get_payment_status")
    
    def get_payment_status(self, order):
        if order.payment:
            return order.payment.status
        else:
            status = "Pay on delivery"
            return status
        
           
    class Meta:
        model = Order
        fields = ('id', 'user', 'name', 'phone', 'address', 'order', 'total')
        
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('id', 'order', 'meal', 'quantity', 'price')
        
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('id', 'order', 'status', 'amount', 'transaction_id', 'payment_method')

class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = ('id', 'order', 'status', 'delivery_date', 'delivery_time', 'delivery_address', 'delivery_phone', 'delivery_note')

