from django.db import models
from employee.models import Accounts
from django.contrib.auth.models import User 

# Create your models here.

# Transactions Table
class Transaction(models.Model):

    TRANSACTION_TYPES = (
        ('deposit', 'Deposit'),
        ('withdraw', 'Withdraw'),
        ('transfer', 'Transfer'),
    )


    id = models.AutoField(primary_key=True)
    account_id = models.ForeignKey(Accounts, on_delete=models.CASCADE, related_name="transactions")
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.FloatField()
    recipient = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='received_transfer', help_text="Only for transfer")
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction {self.id} - Account {self.account_id.account_number}"
    