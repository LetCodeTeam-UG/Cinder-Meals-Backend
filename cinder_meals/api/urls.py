from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('auth/register/',views.RegisterAPI.as_view()),
    path('auth/login/',views.LoginAPI.as_view()),
    path('auth/logout/',views.LoginAPI.as_view()),
    # path('auth/user/')
]
