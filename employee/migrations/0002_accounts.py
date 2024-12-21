# Generated by Django 5.0.1 on 2024-12-16 02:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Accounts',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('account_number', models.CharField(max_length=50, unique=True)),
                ('firstname', models.CharField(max_length=250)),
                ('middlename', models.CharField(blank=True, max_length=250, null=True)),
                ('lastname', models.CharField(max_length=250)),
                ('email', models.TextField(blank=True, null=True)),
                ('password', models.TextField()),
                ('pin', models.TextField()),
                ('balance', models.FloatField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]