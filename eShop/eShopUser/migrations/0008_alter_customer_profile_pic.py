# Generated by Django 3.2 on 2021-06-04 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eShopUser', '0007_alter_order_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pic/CustomerProfilePic/'),
        ),
    ]
