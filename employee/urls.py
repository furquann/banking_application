from django.urls import path
from . import views
from users.views import admin_login, admin_logout

urlpatterns = [
    path('', views.bank_dashboard, name='home'),
    path('dashboard/', views.bank_dashboard, name='bank_dashboard'),

    path('create_account/', views.create_account, name='create_account'),
    path('manage_accounts/', views.manage_accounts, name='manage_accounts'),
    path('manage_accounts/edit/<int:account_id>/', views.edit_account, name='edit_account'),
    path('manage_accounts/delete/<int:account_id>/', views.delete_account, name='delete_account'),

    path('transactions/', views.transactions, name='transactions_in_bank'),

    path('announcements/', views.announcement, name='announcements'),
    path('new_announcement/', views.new_announcement, name='new_announcement'),
    path('announcements/edit/<int:announcement_id>/', views.edit_announcement, name='edit_announcement'),
    path('announcement/delete/<int:announcement_id>/', views.delete_announcement, name='delete_announcement'),


    path('login/', admin_login, name="admin_login"),
    path('logout/', admin_logout, name="admin_logout"),
]
