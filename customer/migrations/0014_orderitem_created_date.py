# Generated by Django 4.2.1 on 2023-07-29 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0013_alter_order_created_datetime'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='created_date',
            field=models.DateField(auto_now=True),
        ),
    ]
