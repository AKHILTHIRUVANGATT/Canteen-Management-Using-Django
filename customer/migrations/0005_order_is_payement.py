# Generated by Django 4.2.1 on 2023-06-17 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0004_rename_payment_done_order_is_completed_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='is_payement',
            field=models.BooleanField(default=False),
        ),
    ]
