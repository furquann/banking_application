from django.contrib import admin
from django.urls import path
from . import views
from users.views import member_login, member_logout

urlpatterns = [
    path('', views.dashboard, name="home"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('transactions/', views.transactions, name="transactions"),
    path('deposit/', views.deposit, name='deposit'),
    path('withdraw/', views.withdraw, name='withdraw'),
    path('transfer/', views.transfer, name='transfer'),
        
    path('login/', member_login, name="member_login"),
    path('logout/', member_logout, name="member_logout"),
]
