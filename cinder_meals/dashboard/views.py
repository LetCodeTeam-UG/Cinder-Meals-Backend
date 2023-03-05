# trunk-ignore(flake8/F401)
from django.shortcuts import render
from django.views import View

class DashboardView(View):
    def get(self, request):
        return render(request, 'pages/dashboard.html')

class LoginView(View):
    def get(self, request):
        return render(request, 'pages/login.html')

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

