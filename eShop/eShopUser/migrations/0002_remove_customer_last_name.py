# Generated by Django 3.2 on 2021-05-07 21:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eShopUser', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='last_name',
        ),
    ]