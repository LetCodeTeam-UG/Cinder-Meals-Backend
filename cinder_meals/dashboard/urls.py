from django.urls import path

from . import views

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('analytics/', views.AnalyticsView.as_view(), name='analytics'),
    path('order/', views.OrderView.as_view(), name='order'),
    path('orders/', views.OrderListView.as_view(), name='orders'),
]
