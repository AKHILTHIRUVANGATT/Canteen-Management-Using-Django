# Generated by Django 4.2.1 on 2023-07-13 01:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_alter_user_mobile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='mobile',
            field=models.CharField(blank=True, error_messages={'unique': 'Mobile number already used'}, null=True, unique=True),
        ),
    ]
