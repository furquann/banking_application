# Generated by Django 5.0.1 on 2024-12-21 08:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_remove_transaction_remarks_transaction_recipient'),
        ('employee', '0005_accounts_user_alter_accounts_id'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='account_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='employee.accounts'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='recipient',
            field=models.ForeignKey(blank=True, help_text='Only for transfer', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='receiveed_transfer', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Account',
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]