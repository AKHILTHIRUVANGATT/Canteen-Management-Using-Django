# Generated by Django 4.2.1 on 2023-07-07 01:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_user_is_waiter_alter_user_is_staff'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, error_messages={'unique': 'Email already exists'}, max_length=254, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='mobile',
            field=models.BigIntegerField(blank=True, error_messages={'max_length': 'Max length exceeded 10', 'unique': 'Mobile number already exists'}, max_length=10, null=True, unique=True),
        ),
    ]
