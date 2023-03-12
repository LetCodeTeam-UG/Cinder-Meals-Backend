from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from accounts.models import User
from cinder_meals.utils.constants import OrderStatus
from django.utils.decorators import method_decorator
from cinder_meals.utils.decorators import AdminAndCourierOnly
from dashboard.models import Meal, Order, DeliveryLocation
from dashboard.forms import DeliveryLocationForm, MealForm

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
        delete_user_id = request.GET.get('delete_user_id')
        edit_user_id = request.GET.get('edit_user_id')
        if delete_user_id:
            try:
                user = User.objects.get(id=delete_user_id)
                user.delete()
                messages.success(request, 'User deleted successfully')
                return redirect(request.META.get('HTTP_REFERER'))
            except Exception as e:
                for error in e.args:
                    messages.error(request, error)
                return redirect(request.META.get('HTTP_REFERER'))
        if edit_user_id:
            user = User.objects.get(id=edit_user_id)
            email = user.email
            context = {
                'user' : user,
                'email' : email,
            }
            return render(request, self.template_name, context)
        
        return render(request, self.template_name)
        
        
    
    def post(self, request):
        user_id = request.POST.get('user_id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        if first_name == None or last_name == None:
            messages.error(request, 'First name and last name are required')
            return render(request, self.template_name)
        else:
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
        print('context')
        if user_id:
            user = User.objects.get(id=user_id).first()
            if user:
                user.fullname = fullname
                user.email = email
                user.phone = phone
                user.gender = gender
                user.dob = dob
            
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
        

class UserProfileView(View):
    @method_decorator(AdminAndCourierOnly)
    def get(self, request):
        return render(request, 'pages/profile.html')
                    
        

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
        orders = Order.objects.all().order_by('-created_at')
        context = {
            'orders' : orders,
        }
        return render(request, 'pages/orders.html', context)
    
class PendingOrderListView(View):
    @method_decorator(AdminAndCourierOnly)
    def get(self, request):
        pending_orders = Order.objects.filter(status=OrderStatus.PENDING.value).order_by('-created_at')
        print(pending_orders)
        context = {
            'pending_orders' : pending_orders,
        }
        return render(request, 'pages/pending_orders.html', context)
    
class CompletedOrderListView(View):
    @method_decorator(AdminAndCourierOnly)
    def get(self, request):
        completed_orders = Order.objects.filter(status=OrderStatus.COMPLETED.value).order_by('-created_at')
        context = {
            'completed_orders' : completed_orders,
        }
        return render(request, 'pages/completed_orders.html', context)
    
class CancelledOrderListView(View):
    @method_decorator(AdminAndCourierOnly)
    def get(self, request):
        cancelled_orders = Order.objects.filter(status=OrderStatus.CANCELLED.value).order_by('-created_at')
        context = {
            'cancelled_orders' : cancelled_orders,
        }
        return render(request, 'pages/cancelled_orders.html', context)

class MealView(View):
    @method_decorator(AdminAndCourierOnly)
    def get(self, request):
        return render(request, 'pages/meal-detail.html')
    
class MealListView(View):
    @method_decorator(AdminAndCourierOnly)
    def get(self, request, *args, **kwargs):
        meals = Meal.objects.filter(published = True).order_by('-id')
        context = {
            'meals' : meals,
        }
        return render(request, 'pages/meals.html',context)
    
    


class AddMealView(View):
    template_name = 'pages/add-meal.html'

    @method_decorator(AdminAndCourierOnly)
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, 'pages/add-meal.html',context)
    
    def post(self, request, *args, **kwargs):
        form = MealForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('dashboard:add-meal')
        
        print(form.errors)
        return redirect ('dashboard:add-meal')



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
    template_name = 'pages/delivery_locations.html'

    @method_decorator(AdminAndCourierOnly)
    def get(self, request, *args, **kwargs):
        delivery_id = request.GET.get('delivery_id')
        if delivery_id:
            delivery = DeliveryLocation.objects.filter(id=delivery_id).first()
            if delivery:
                delivery.delete()
                messages.success(request, 'Delivery location deleted successfully')
                return redirect('dashboard:delivery_locations')
            else:
                messages.error(request, 'Delivery location does not exist')
                return redirect('dashboard:delivery_locations')
        delivery_details = DeliveryLocation.objects.all()
        context = {
            'delivery_details': delivery_details
        }
        return render(request, self.template_name, context)
    
    def post(self,request, *args, **kwargs):
        location_id = request.POST.get('location_id')
        if location_id:
            location = DeliveryLocation.objects.filter(id=location_id).first()
            if location:
                location.name = request.POST.get('name')
                location.delivery_fee = request.POST.get('delivery_fee')
                location.save()
                messages.success(request, 'Delivery location updated successfully')
                return redirect('dashboard:delivery_locations')
            else:
                messages.error(request, 'Delivery location does not exist')
                return redirect('dashboard:delivery_locations')
        form = DeliveryLocationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Delivery location added successfully')
            return redirect('dashboard:delivery_locations')

        return redirect('dashboard:delivery_locations')
    
    
# class MealsView(View):
#     template_name = 'pages/meals.html'
  
#     def get(self, request, *args, **kwargs):
#         meals = Meal.objects.all()
#         context = {
#             'meals': meals
#         }
#         return render(request, self.template_name, context)

#     def post(self,request, *args, **kwargs):
#         form = DeliveryLocationForm(request.POST)

#         if form.is_valid():
#             form.save()
#             return redirect('dashboard:delivery_locations')

#         print(form.errors) 
#         return redirect('dashboard:delivery_locations')