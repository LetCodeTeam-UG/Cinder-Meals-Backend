import time
from django.db import models
# trunk-ignore(flake8/F401)
from cinder_meals.utils.constants import  MealType, OrderStatus, PaymentMethod

# Information about the restaurant
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

# Banner for the home page
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

# Meals sold by the restaurant
class Meal(models.Model):
    title = models.CharField(max_length=50)
    type = models.CharField(max_length=10, default=MealType.ANY.value)
    description = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.ImageField(upload_to='meals/images/')
    orders_count = models.IntegerField(default = 0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    published = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
    

    class Meta:
        db_table = 'meals'
    
        

# Oder items for the customer
class OrderItem(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    quantity = models.IntegerField(default = 1)
    total = models.DecimalField(max_digits=5, decimal_places=2,null=True, blank=True)
    allergies = models.CharField(max_length = 200, null = True, blank = True)
    additional_info = models.CharField(max_length = 200, null = True, blank = True)

    class Meta:
        db_table = 'order_items'
    
    def get_total(self):
        return self.quantity * self.meal.price
    
    def __str__(self):
        return self.meal.title

# Customer's Order Information
class Order(models.Model):
    def get_id():
        return int(round(time.time() * 1000))
    order_id =  models.CharField(max_length=20, default=get_id)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    order_items = models.ManyToManyField(OrderItem)
    sub_total = models.DecimalField(max_digits=5, decimal_places=2,null=True, blank=True)
    total = models.DecimalField(max_digits=5, decimal_places=2,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    phone = models.CharField(max_length=20)
    location = models.ForeignKey('DeliveryLocation', on_delete=models.SET_NULL, null=True)
    order_note = models.CharField(max_length=200, null=True, blank=True)
    payment_method = models.CharField(max_length=15, default=PaymentMethod.MOBILE_MONEY.value)
    approved = models.BooleanField(default=False)
    status = models.CharField(max_length=10, default=OrderStatus.PENDING.value) 
    
    def set_total(self):
        self.total = self.get_order_items_total()
        self.save()
    
    def get_order_items(self):
        order_items = []
        for order_item in self.order_items.all():
            order_items.append(order_item)
        return order_items
    
    def get_order_items_count(self):
        count = 0
        for order_item in self.order_items.all():
            count += order_item.quantity
        return count
    
    def get_order_items_total(self):
        total = 0
        for order_item in self.order_items.all():
            total += order_item.get_total()
        return total
    
    def __str__(self):
        return self.order_id
    
    # def save(self, *args, **kwargs):
    #         super().save(*args, **kwargs)

    #         # Calculate the sub total and total
    #         self.sub_total = sum(item.meal.price for item in self.order_items.all())
    #         print(self.sub_total)
    #         if self.location:
    #             self.total = self.sub_total + self.location.delivery_fee
    #         else:
    #             self.total = self.sub_total

    #         # Save the order items
    #         self.order_items.set(list(self.order_items.all()))

class Delivery(models.Model):
    courier = models.ForeignKey('accounts.user.is_courier', on_delete=models.CASCADE)
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, default=OrderStatus.PENDING.value) 

    
    def __str__(self):
        return self.name

# Make Payment Momo
class Payment(models.Model):
    def get_payment_id(self):
        return int(round(time.time() * 10000))
    payment_id =  models.CharField(max_length=12, default=get_payment_id)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    network = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10)

    def __str__(self):
        return self.name

# Address Information
class DeliveryLocation(models.Model):
    name = models.CharField(max_length=200)
    delivery_fee = models.DecimalField(max_digits=5, decimal_places=2)
    
    def __str__(self):
        return self.name
