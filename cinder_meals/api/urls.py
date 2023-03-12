from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('auth/register/',views.RegisterAPI.as_view()),
    path('auth/login/',views.LoginAPI.as_view()),
    path('auth/logout/',views.LogoutAPI.as_view()),
    # path('auth/user/')
    
    path('meals/',views.MealListAPI.as_view()),
    path('order/list_create_order/',views.OrderAPIView.as_view()),
]
