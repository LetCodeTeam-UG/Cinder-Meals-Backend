from rest_framework import serializers
from accounts.models import User
from dashboard.models import Order, Delivery, Payment,Meal, OrderItem, Banner, Restaurant
from django.contrib.auth import authenticate
from django.conf import settings

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'fullname', 'username', 'email', 'gender', 'phone')

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ( 'fullname', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'gender', 'phone')

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ('id', 'title', 'image')




class MealSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Meal
        fields = ['id', 'name', 'description', 'image', 'image_url', 'created_at', 'updated_at', 'published']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None
    
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('user', 'order_items', 'total', 'created_at', 'phone', 'location', 'payment_method', 'status')
        
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('user', 'meal', 'allergies', 'additional_info')
        
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('order', 'status', 'amount', 'transaction_id', 'payment_method')

class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = ('order', 'status', 'delivery_date', 'delivery_time', 'delivery_address', 'delivery_phone', 'delivery_note')

