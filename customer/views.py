from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from employee.models import Accounts
from .models import Transaction
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q

# Create your views here.

@login_required(login_url='/login/')
def transactions(request):
    current_user = request.user
    search_query = request.GET.get("query", "").strip()

    # Filter transactions where the user is involved (either as account holder or recipient)
    transactions = Transaction.objects.filter(
        Q(account_id__user=current_user) |  # Transactions related to user's account
        Q(recipient=current_user)          # Transactions where the user is a recipient
    )

    # Apply search filter if query is provided
    if search_query:
        transactions = transactions.filter(
            Q(account_id__account_number__icontains=search_query) |
            Q(type__icontains=search_query)
        )

    # Paginate the transactions
    paginator = Paginator(transactions.order_by("-date_created"), 10)  # Show 10 entries per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Render the template with context
    context = {
        "transactions": page_obj,
        "search_query": search_query,
    }
    return render(request, "customer/transaction.html", context)

@login_required(login_url='/login/')
def deposit(request):
    if request.method == 'POST':
        deposited_amount = float(request.POST.get('deposited_amount'))

        try:
            account = Accounts.objects.get(user=request.user)
            account.balance += deposited_amount
            account.save()

            Transaction.objects.create(
                account_id=account,
                type='deposit',
                amount=deposited_amount
            )

            messages.success(request, f"Successfully deposited ₹{deposited_amount} into account {account}.")
        except Accounts.DoesNotExist:
            messages.error(request, "Account number not found.")
        
        return redirect('deposit')  

    # Assuming 'Account' model has a method to get the balance of an account
    balance = 0
    if request.user.is_authenticated:
        # Example: Retrieve balance based on the logged-in user's account (modify based on your logic)
        try:
            account = Accounts.objects.get(user=request.user)
            balance = account.balance
            account_number = account.account_number

        except Accounts.DoesNotExist:
            balance = 0

    return render(request, 'customer/deposit.html', {'balance': balance, 'account_number': account_number})


@login_required(login_url='/login/')
def withdraw(request):
    if request.method == 'POST':
        withdraw_amount = request.POST.get('withdraw_amount')

        try:
            withdraw_amount = float(withdraw_amount)
            if withdraw_amount <= 0:
                messages.error(request, "Withdrawal amount must be greater than zero.")
                return redirect('withdraw')

            # Get the logged-in user's account
            account = Accounts.objects.get(user=request.user)

            if account.balance >= withdraw_amount:
                account.balance -= withdraw_amount
                account.save()

                Transaction.objects.create(
                    account_id=account,
                    type='withdraw',
                    amount=withdraw_amount
                )

                messages.success(request, f"Successfully withdrew ₹{withdraw_amount:.2f} from your account.")
            else:
                messages.error(request, "Insufficient balance.")
        except ValueError:
            messages.error(request, "Invalid withdrawal amount.")
        except Accounts.DoesNotExist:
            messages.error(request, "Account not found. Please contact support.")
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {str(e)}")
        
        return redirect('withdraw')

    # Display the account balance for GET requests
    balance = 0
    account_number = None
    if request.user.is_authenticated:
        try:
            account = Accounts.objects.get(user=request.user)
            balance = account.balance
            account_number = account.account_number
        except Accounts.DoesNotExist:
            messages.error(request, "No account found for the logged-in user. Please contact support.")

    return render(request, 'customer/withdraw.html', {'balance': balance, 'account_number': account_number})


@login_required(login_url='/login/')
def transfer(request):
    if request.method == 'POST':
        reciever_account_number = request.POST.get('reciever_account_number')
        reciever_name = request.POST.get('reciever_name')
        transfer_amount = float(request.POST.get('transfer_amount'))

        try:
            sender_account = Accounts.objects.get(user=request.user)
            reciever_account = Accounts.objects.get(account_number=reciever_account_number)
            reciever_account = Accounts.objects.get(account_number=reciever_account_number)
            recipient_user = reciever_account.user

            if sender_account.balance >= transfer_amount:
                sender_account.balance -= transfer_amount
                reciever_account.balance += transfer_amount

                sender_account.save()
                reciever_account.save()

                Transaction.objects.create(
                    account_id=sender_account,
                    type='transfer',
                    amount=transfer_amount,
                    recipient=recipient_user
                )

                messages.success(request, f"Successfully transferred ₹{transfer_amount} to {reciever_name}'s account.")
            else:
                messages.error(request, "Insufficient balance for the transfer.")
        except Accounts.DoesNotExist:
            messages.error(request, "One or both account numbers not found.")
        
        return redirect('transfer')  

    balance = 0
    if request.user.is_authenticated:
        try:
            account = Accounts.objects.get(user=request.user)
            balance = account.balance
            account_number = account.account_number
        except Accounts.DoesNotExist:
            balance = 0

    return render(request, 'customer/transfer.html', {'balance': balance, 'account_number': account_number})


@login_required(login_url='/login/')
def dashboard(request):
    try:
        if not request.user.is_authenticated:
            return redirect('member_login')
            
        account = Accounts.objects.filter(user=request.user).first()
        
        if not account:
            messages.error(request, "No banking account found for this user. Please contact support.")
            return redirect('member_login')
        
        context = {
            'page_title': 'Dashboard',
            'account_number': account.account_number,
            'account_balance': '{:,.2f}'.format(account.balance),
            'full_name': f"{account.first_name} {account.middle_name or ''} {account.last_name}".strip(),
        }
        
        return render(request, 'customer/dashboard.html', context)
    
    except Exception as e:
        print(f"Error in dashboard view: {str(e)}")  # Debug print
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect('member_login')
