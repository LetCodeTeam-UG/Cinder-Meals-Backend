from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from accounts.models import User
from cinder_meals.utils.constants import OrderStatus
from django.utils.decorators import method_decorator
from cinder_meals.utils.decorators import AdminAndCourierOnly
from dashboard.models import Meal, Order, DeliveryLocation
from dashboard.forms import DeliveryLocationForm

class DashboardView(View):
    @method_decorator(AdminAndCourierOnly)
    def get(self, request):
        most_selling_meals = Meal.objects.filter(published = True).order_by('-orders_count')[:5]
        meal_count = Meal.objects.filter(published=True).order_by('-id').count()
        orders_count = Order.objects.all().count()
        total_customers = User.objects.filter(is_customer=True).count()
        total_pending_orders = Order.objects.filter(status=OrderStatus.PENDING.value).count()
        orders_on_delivery_count = Order.objects.filter(status=OrderStatus.ON_THE_WAY.value).count()
        orders_delivered_count = Order.objects.filter(status=OrderStatus.COMPLETED.value).count()
        orders_cancelled_count = Order.objects.filter(status=OrderStatus.CANCELLED.value).count()
        context = {
            'most_selling_meals' : most_selling_meals,
            'meal_count' : meal_count,
            'orders_count' : orders_count,
            'total_pending_orders' : total_pending_orders,
            'total_customers' : total_customers,
            'orders_on_delivery_count' : orders_on_delivery_count,
            'orders_delivered_count' : orders_delivered_count,
            'orders_cancelled_count' : orders_cancelled_count,
        }
        return render(request, 'pages/dashboard.html', context)
    
class CreateUpdateUserView(View):
    template_name = 'pages/create-update-user.html'
    @method_decorator(AdminAndCourierOnly)
    def get(self, request):
        user_id = request.GET.get('user_id')
        if user_id:
            try:
                user = User.objects.get(id=user_id)
                user.delete()
                messages.success(request, 'User deleted successfully')
                return redirect(request.META.get('HTTP_REFERER'))
            except Exception as e:
                for error in e.args:
                    messages.error(request, error)
                return redirect(request.META.get('HTTP_REFERER'))
        else:
            return render(request, self.template_name)
    
    def post(self, request):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        fullname = first_name + ' ' + last_name
        email = request.POST.get('email')
        phone = request.POST.get('phone_number')
        role = request.POST.get('group')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        password = request.POST.get('password')
        confirm = request.POST.get('confirm')
        is_active = request.POST.get('is_active')
        context = {k : v for k, v in request.POST.items()}
        try: 
            user = User.objects.filter(email=email).first()
            if user:
                messages.error(request, 'User with this email already exists')
                return render(request, self.template_name, context)
            
            else:
                if password == confirm:
                    user = User.objects.create_user(
                        fullname=fullname,
                        email=email,
                        phone=phone,
                        gender=gender,
                        dob=dob,
                        password=password,
                    )
                    if role == 'Admin':
                        user.is_admin = True
                    elif role == 'Courier':
                        user.is_courier = True
                    elif role == 'Customer':
                        user.is_customer = True
                    user.save()
                    messages.success(request, 'User created successfully')
                    redirect_url = reverse('dashboard:users')
                    return redirect(redirect_url)
                
                else:
                    messages.error(request, 'Passwords do not match')
                    return render(request, self.template_name, context)
        except Exception as e:
            for error in e.args:
                messages.error(request, error)
            return render(request, self.template_name, context)
        

        
                    
        

class AnalyticsView(View):
    @method_decorator(AdminAndCourierOnly)
    def get(self, request):
        return render(request, 'pages/analytics.html')

class OrderView(View):
    @method_decorator(AdminAndCourierOnly)
    def get(self, request):
        return render(request, 'pages/order-detail.html')
    
class OrderListView(View):
    @method_decorator(AdminAndCourierOnly)
    def get(self, request):
        return render(request, 'pages/orders.html')
    
class PendingOrderListView(View):
    @method_decorator(AdminAndCourierOnly)
    def get(self, request):
        return render(request, 'pages/pending_orders.html')
    
class CompletedOrderListView(View):
    @method_decorator(AdminAndCourierOnly)
    def get(self, request):
        return render(request, 'pages/completed_orders.html')
class CancelledOrderListView(View):
    @method_decorator(AdminAndCourierOnly)
    def get(self, request):
        return render(request, 'pages/cancelled_orders.html')

class MealView(View):
    @method_decorator(AdminAndCourierOnly)
    def get(self, request):
        return render(request, 'pages/meal-detail.html')
    
class MealListView(View):
    @method_decorator(AdminAndCourierOnly)
    def get(self, request):
        meals = Meal.objects.filter(published = True).order_by('-id')
        context = {
            'meals' : meals,
        }
        return render(request, 'pages/meals.html',context)

class CustomersView(View):
    @method_decorator(AdminAndCourierOnly)
    def get(self, request):
        customers = User.objects.filter(is_customer=True).order_by("-id")
        context = {
            "customers":customers,
        }
        return render(request, 'pages/customers.html',context)  

class CouriersView(View):
    @method_decorator(AdminAndCourierOnly)
    def get(self, request):
        courier = User.objects.filter(is_courier=True).order_by("-id")
        context = {
            "courier":courier,
        }
        return render(request, 'pages/couriers.html',context)  

class UsersView(View):
    @method_decorator(AdminAndCourierOnly)
    def get(self, request):
        users = User.objects.all().order_by('-id')
        context = {
            "users":users,
        }
        return render(request, 'pages/users.html', context)


class DeliveryLocationView(View):
    template_name = 'pages/delivery-location.html'
  
    def get(self, request, *args, **kwargs):
        delivery_details = DeliveryLocation.objects.all()
        context = {
            'delivery_details': delivery_details
        }
        return render(request, self.template_name, context)

    def post(self,request, *args, **kwargs):
        form = DeliveryLocationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('dashboard:delivery-locations')

        print(form.errors) 
        return redirect('dashboard:delivery-locations')