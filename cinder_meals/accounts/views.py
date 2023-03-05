from django.shortcuts import render
from django.contrib import messages
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from accounts.models import User
class LoginView(View):
    template_name = 'login.html'
    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        remember_me = "on" if request.POST.get('remember_me') else "off"
        user = authenticate(request, email=email, password=password)
        if user is not None:
            if  user.is_admin or user.is_courier:
                login(request, user)
                redirect_url = request.GET.get('next', 'dashboard:dashboard')
                return redirect(redirect_url)
            else:
                context = {k : v for k, v in request.POST.items()}
                messages.error(request, "You're Not Authorized")
                return render(request, self.template_name, context)
        else:
            context = {k : v for k, v in request.POST.items()}
            print(context)
            messages.error(request, "Invalid credentials")
            return render(request, self.template_name, context)