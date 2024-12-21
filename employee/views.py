from django.shortcuts import render, redirect, get_object_or_404
import random
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from . models import Announcement, Accounts
from django.urls import reverse
from django.db.models import Q, Sum
from django.contrib.auth.models import User
from .utils import generate_unique_account_number
from customer.models import Transaction
from django.core.paginator import Paginator


# Create your views here.

@user_passes_test(lambda u: u.is_superuser, login_url='/staff/login/')
def bank_dashboard(request):
    # Calculate the required statistics
    accounts_count = Accounts.objects.count()  
    total_balance = Accounts.objects.aggregate(total_balance=Sum('balance'))['total_balance']
    total_transactions = Transaction.objects.count()  

    # Pass the data to the template context
    context = {
        'accounts_count': accounts_count,
        'total_balance': total_balance or 0,  # Default to 0 if no accounts exist
        'total_transactions': total_transactions
    }

    return render(request, 'employee/dashboard.html', context)



@user_passes_test(lambda u: u.is_superuser, login_url='/staff/login/')
def user_account(request):
    return render(request, 'employee/settings.html')



@user_passes_test(lambda u: u.is_superuser, login_url='/staff/login/')
def create_account(request):

    if request.method == 'POST':
        account_number = request.POST.get('account_number')
        first_name = request.POST.get('first_name')
        middle_name = request.POST.get('middle_name') 
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        pin = request.POST.get('pin')
        beginning_balance = request.POST.get('beginning_balance')

        # Validate the input data (basic validation)
        errors = []
        if not first_name or not last_name or not email or not password or not pin or not beginning_balance:
            errors.append("All required fields must be filled.")

        if len(pin) != 4 or not pin.isdigit():
            errors.append("Pin must be a 4-digit number.")

        if errors:
            messages.error(request, " ".join(errors))
            return render(request, 'employee/create_account.html', {
                'account_number': account_number,
            })

        # Save the data to the database
        try:
            account = Accounts(
                account_number=account_number,
                first_name=first_name,
                middle_name=middle_name,
                last_name=last_name,
                email=email,
                password=password,  
                pin=pin,
                balance=beginning_balance,
            )
            account.save()
            messages.success(request, "Account created successfully!")
            return redirect('manage_accounts') 
        
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return render(request, 'employee/create_account.html', {
                'account_number': account_number,
            })
        
    generated_account_number = generate_unique_account_number()
    return render(request, 'employee/create_account.html', {'account_number': generated_account_number})        


@user_passes_test(lambda u: u.is_superuser, login_url='/staff/login/')
def manage_accounts(request):
    query = request.GET.get("query")
    accounts = Accounts.objects.all()

    if query:
        accounts = accounts.filter(
            Q(account_number__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query)
        )

    context = {
        "accounts": accounts
    }

    return render(request, 'employee/manage_accounts.html', context)


@user_passes_test(lambda u: u.is_superuser, login_url='/staff/login/')
def edit_account(request, account_id):
    account = get_object_or_404(Accounts, id=account_id) 

    if request.method == 'POST':
        account_number = request.POST.get('account_number')
        first_name = request.POST.get('first_name')
        middle_name = request.POST.get('middle_name', '')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        pin = request.POST.get('pin')
        beginning_balance = request.POST.get('beginning_balance')

        # Validation: Check if all required fields are filled
        if not all([account_number, first_name, last_name, email, pin, beginning_balance]):
            messages.error(request, "All fields are required.")
            return render(request, 'employee/edit_account.html', {'account': account})

        # Update account fields
        account.account_number = account_number
        account.first_name = first_name
        account.middle_name = middle_name
        account.last_name = last_name
        account.email = email
        if password:  
            account.password = password 
        account.pin = pin
        account.balance = beginning_balance

        # Save the updated account
        account.save()

        messages.success(request, "Account updated successfully.")
        return redirect(reverse('manage_accounts')) 

    # Prepopulate form with existing data
    return render(request, 'employee/edit_account.html', {'account': account})


@user_passes_test(lambda u: u.is_superuser, login_url='/staff/login/')
def delete_account(request, account_id):

    account = get_object_or_404(Accounts, id=account_id)

    if request.method == 'POST':
        account.delete()
        messages.success(request, "Account deleted successfully.")
        return redirect(reverse('manage_accounts')) 

    return render(request, 'employee/delete_account.html', {'account': account})


@user_passes_test(lambda u: u.is_superuser, login_url='/staff/login/')
def transactions(request):
    query = request.GET.get("query", "")
    entries_per_page = request.GET.get("entries", 10)

    try:
        entries_per_page = int(entries_per_page)
        if entries_per_page <= 0:
            entries_per_page = 10
    except ValueError:
        entries_per_page = 10

    transactions = Transaction.objects.filter(
        Q(account_id__account_number__icontains=query) |  # Search by account number
        Q(type__icontains=query) |                       # Search by transaction type
        Q(recipient__username__icontains=query)          # Search by recipient username
    ).order_by("-date_created")

    paginator = Paginator(transactions, entries_per_page)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "query": query,
        "entries_per_page": entries_per_page,
    }

    return render(request, "employee/transactions.html", context)


@user_passes_test(lambda u: u.is_superuser, login_url='/staff/login/')
def announcement(request):
    announcements = Announcement.objects.all().order_by('-date_updated')
    return render(request, 'employee/announcement.html', {'announcements': announcements})


@user_passes_test(lambda u: u.is_superuser, login_url='/staff/login/')
def new_announcement(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        announcement_body = request.POST.get('announcement')
        
        # Create a new announcement
        announcement = Announcement.objects.create(
            title=title,
            announcement=announcement_body
        )
        messages.success(request, "Created new announcement")
        return redirect('announcements')

    return render(request, 'employee/new_announcement.html')


@user_passes_test(lambda u: u.is_superuser, login_url='/staff/login/')
def edit_announcement(request, announcement_id):
    announcement = get_object_or_404(Announcement, id=announcement_id)

    if request.method == 'POST':
        title = request.POST.get('title')
        body = request.POST.get('announcement')

        if title and body:
            announcement.title = title
            announcement.announcement = body
            announcement.save()
            return redirect('announcements')  

    context = {
        'title': announcement.title,
        'body': announcement.announcement,
    }
    return render(request, 'employee/edit_announcement.html', context)


@user_passes_test(lambda u: u.is_superuser, login_url='/staff/login/')
def delete_announcement(request, announcement_id):

    announcement = get_object_or_404(Announcement, id=announcement_id)

    if request.method == 'POST':
        announcement.delete()
        messages.success(request, "Announcement Deleted")
        return redirect('announcements')
    
    return render(request, 'employee/delete_confirmation.html', {'announcement': announcement})
