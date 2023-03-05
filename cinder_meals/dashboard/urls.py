from django.urls import path

from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('analytics/', views.AnalyticsView.as_view(), name='analytics'),
    path('order/', views.OrderView.as_view(), name='order'),
    path('orders/', views.OrderListView.as_view(), name='orders'),
    path('meal/', views.MealView.as_view(), name='meal'),
    path('meals/', views.MealListView.as_view(), name='meals'),
    path('customers/', views.CustomersView.as_view(), name='customers'),
    path('users/', views.UsersView.as_view(), name='users'),
    path('create_update_user/', views.CreateUpdateUserView.as_view(), name= 'create/update user'),
]