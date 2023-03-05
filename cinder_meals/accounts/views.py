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

class ForgotPasswordView(View):
    def get(self, request):
        return render(request, 'forgot-password.html')
    def post(self, request):
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            user.send_password_reset_email()
            messages.success(request, "Password reset link sent to your email")
        else:
            messages.error(request, "User with this email does not exist")
        return redirect('accounts:login')
    
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('accounts:login')