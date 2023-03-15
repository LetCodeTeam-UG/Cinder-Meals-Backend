from django.contrib import messages
from django.shortcuts import redirect, reverse


class AdminAndCourierOnly:
    def __init__(self, func):
       self.func = func
       
    def __call__(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to view this page")
            return redirect(reverse("accounts:login"))
        if not request.user.is_admin and not request.user.is_courier and not request.user.is_superuser and not request.user.is_staff and not request.user.is_active:
            messages.error(request, "You do not have permission to view this page")
            return redirect(reverse("accounts:login"))
        return self.func(request, *args, **kwargs)