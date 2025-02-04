# Generated by Django 4.2.1 on 2023-06-04 15:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('is_deleted', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
                'db_table': 'manager_category',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('image', models.ImageField(upload_to='menu')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('offer', models.IntegerField()),
                ('description', models.CharField(max_length=255)),
                ('is_deleted', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('category', models.ForeignKey(limit_choices_to={'is_delete': False}, on_delete=django.db.models.deletion.CASCADE, to='manager.category')),
            ],
            options={
                'verbose_name': 'menu',
                'verbose_name_plural': 'menus',
                'db_table': 'manager_menu',
                'ordering': ('id',),
            },
        ),
    ]
