import time
import random
from django.db import models
from cinder_meals.utils.constants import  MealType, OrderStatus, PaymentMethod, PaymentStatus

class Restaurant(models.Model):
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    description = models.CharField(max_length=200)
    image = models.ImageField(upload_to='restaurants/images/')
    facebook = models.URLField(default="https://www.facebook.com/")
    twitter = models.URLField(default="https/www.twitter.com/")
    instagram = models.URLField(default='https://www.instagram.com/')
    
    def __str__(self):
        return self.name

class Banner(models.Model):
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to='banners/images/')
    published = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'banners'
    
    def __str__(self):
        return self.title
    
    def publish(self):
        self.published = True
        self.save()
    
    def unpublish(self):
        self.published = False
        self.save()
    
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        return ""

class Meal(models.Model):
    title = models.CharField(max_length=50)
    type = models.CharField(max_length=10, default=MealType.ANY)
    description = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.ImageField(upload_to='meals/images/')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    published = models.BooleanField(default=False)
    def __str__(self):
        return self.title

class OrderItem(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    
    class Meta:
        db_table = 'order_items'
    
    def get_total(self):
        return self.quantity * self.price
    
    def __str__(self):
        return self.meal.title

class Order(models.Model):
    def get_id(self):
        return int(round(time.time() * 1000))
    order_id =  models.CharField(max_length=20, default=get_id)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    orderitems = models.ManyToManyField(OrderItem)
    total = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    phone = models.CharField(max_length=20)
    payment_method = models.CharField(max_length=10, default=PaymentMethod.MOBILE_MONEY)
    approved = models.BooleanField(default=False)
    status = models.CharField(max_length=10, default=OrderStatus.PENDING)
    
    def get_order_items(self):
        order_items = []
        for order_item in self.orderitems.all():
            order_items.append(order_item)
        return order_items
    
    def get_order_items_count(self):
        count = 0
        for order_item in self.orderitems.all():
            count += order_item.quantity
        return count
    
    def get_order_items_total(self):
        total = 0
        for order_item in self.orderitems.all():
            total += order_item.get_total()
        return total
        
    def is_approved(self):
        self.status = OrderStatus.APPROVED
        self.approved = True
        self.save()
        return self.status
    
    def is_completed(self):
        self.status = OrderStatus.COMPLETED
        self.save()
        return self.status
    
    def is_cancelled(self):
        self.status = OrderStatus.CANCELLED
        self.save()
        return self.status
    
    def on_delivery(self):
        self.status = OrderStatus.ON_THE_WAY
        self.save()
        return self.status
    
    def __str__(self):
        return self.order_id

class Delivery(models.Model):
    name = models.CharField(max_length=50)
    courier = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    order = models.TextField()
    total = models.DecimalField(max_digits=5, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10)
    
    def __str__(self):
        return self.name

class Payment(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    order = models.TextField()
    total = models.DecimalField(max_digits=5, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class Address(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    note = models.CharField(max_length=200)

