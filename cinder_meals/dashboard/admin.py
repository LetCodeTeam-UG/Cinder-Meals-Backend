from django.contrib import admin

from dashboard.models import *

admin.site.register(Meal)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(DeliveryLocation)
admin.site.register(Payment)
admin.site.register(Delivery)

