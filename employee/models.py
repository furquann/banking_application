from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

# SystemInfo Table
class SystemInfo(models.Model):
    id = models.AutoField(primary_key=True)
    meta_field = models.TextField()
    meta_value = models.TextField()

    def __str__(self):
        return f"{self.meta_field} - {self.meta_value}"



# Accounts Table
class Accounts(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    account_number = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=250)
    middle_name = models.CharField(max_length=250, blank=True, null=True)
    last_name = models.CharField(max_length=250)
    email = models.TextField(blank=True, null=True)
    password = models.TextField()
    pin = models.TextField()
    balance = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.account_number





   


# Announcements Table
class Announcement(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.TextField()
    announcement = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    

@receiver(post_save, sender=Accounts)
def create_user_for_account(sender, instance, created, **kwargs):

    if created:
        user = User.objects.create_user(
            username=instance.account_number,
            email=instance.email,
            password=instance.password
        )

        instance.user = user
        instance.save()