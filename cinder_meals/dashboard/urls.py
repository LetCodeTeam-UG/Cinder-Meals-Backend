from django.urls import path

from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('analytics/', views.AnalyticsView.as_view(), name='analytics'),
    path('order/', views.OrderView.as_view(), name='order'),
    path('orders/', views.OrderListView.as_view(), name='orders'),
    path('orders/order_detail/', views.OrderDetailView.as_view(), name='order_detail'),
    path('orders/pending_orders/', views.PendingOrderListView.as_view(), name='pending_orders'),
    path('orders/completed_orders/', views.CompletedOrderListView.as_view(), name='completed_orders'),
    path('orders/cancelled_orders/', views.CancelledOrderListView.as_view(), name='cancelled_orders'),
    path('meal/', views.MealView.as_view(), name='meal'),
    path('meals/', views.MealListView.as_view(), name='meals'),
    path('add-meal/', views.AddMealView.as_view(), name='add-meal'),
    path('customers/', views.CustomersView.as_view(), name='customers'),
    path('couriers/', views.CouriersView.as_view(), name='couriers'),
    path('users/', views.UsersView.as_view(), name='users'),
    path('delivery_locations/', views.DeliveryLocationView.as_view(), name='delivery_locations'),
    path('create_update_user/', views.CreateUpdateUserView.as_view(), name= 'create_update_user'),
    path('profile/',views.UserProfileView.as_view(), name='profile'),
    path('profile/update/',views.UpdateProfileView.as_view(), name='update_profile'),
    path('profile/change_password/',views.ChangePasswordView.as_view(), name='change_password'),
]
