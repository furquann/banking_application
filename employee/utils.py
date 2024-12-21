from . models import Accounts


def generate_unique_account_number():

    last_account = Accounts.objects.order_by('account_number').last()

    if last_account is None:
        new_account_number = 1000000000000001  # Start with a defined initial value
    else:
        new_account_number = int(last_account.account_number) + 1

    return str(new_account_number)
