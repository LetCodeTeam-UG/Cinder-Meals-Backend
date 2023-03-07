# trunk-ignore(flake8/F401)
from django.shortcuts import render
from django.views import View
from accounts.models import User
from cinder_meals.utils.constants import OrderStatus
from django.utils.decorators import method_decorator
from cinder_meals.utils.decorators import AdminAndCourierOnly
from dashboard.models import Meal, Order

class DashboardView(View):
    @method_decorator(AdminAndCourierOnly)
    def get(self, request):
        most_selling_meals = Meal.objects.filter(published = True).order_by('-orders_count')[:5]
        meal_count = Meal.objects.filter(published=True).order_by('-id').count()
        orders_count = Order.objects.all().count()
        total_customers = User.objects.filter(is_customer=True).count()
        total_pending_orders = Order.objects.filter(status=OrderStatus.PENDING).count()
        orders_on_delivery_count = Order.objects.filter(status=OrderStatus.ON_DELIVERY).count()
        orders_delivered_count = Order.objects.filter(status=OrderStatus.DELIVERED).count()
        orders_cancelled_count = Order.objects.filter(status=OrderStatus.CANCELLED).count()
        context = {
            'most_selling_meals' : most_selling_meals,
            'meal_count' : meal_count,
            'orders_count' : orders_count,
            'total_pending_orders' : total_pending_orders,
            'total_customers' : total_customers,
        }
        return render(request, 'pages/dashboard.html', context)
    
class CreateUpdateUserView(View):
    def get(self, request):
        return render(request, 'pages/create-update-user.html')

class AnalyticsView(View):
    def get(self, request):
        return render(request, 'pages/analytics.html')

class OrderView(View):
    def get(self, request):
        return render(request, 'pages/order-detail.html')
class OrderListView(View):
    def get(self, request):
        return render(request, 'pages/orders.html')

class MealView(View):
    def get(self, request):
        return render(request, 'pages/meal-detail.html')
    
class MealListView(View):
    def get(self, request):
        return render(request, 'pages/meals.html')

class CustomersView(View):
    def get(self, request):
        return render(request, 'pages/customers.html')  

class UsersView(View):
    def get(self, request):
        return render(request, 'pages/users.html')
