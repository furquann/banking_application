from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib import messages

#create your views here

def admin_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_superuser:  # Allow only superusers
                login(request, user)
                return redirect("bank_dashboard")  # Redirect to admin dashboard
            else:
                messages.error(request, "You do not have admin permissions.")
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "employee/login.html") 


def admin_logout(request):
    logout(request)
    return redirect("admin_login") 



def member_login(request):
    if request.method == "POST":
        username = request.POST.get("account_number")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        print(f"{username}:  {password}")
        if user is not None:
            if not user.is_superuser:  # Ensure it's not a superuser
                login(request, user)
                return redirect("dashboard")  # Redirect to user dashboard
            else:
                messages.error(request, "Admins must log in at the admin portal.")
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "customer/login.html")  # Replace with your template path


def member_logout(request):
    logout(request)  
    return redirect("member_login")  
