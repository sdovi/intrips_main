# Generated by Django 5.1.5 on 2025-02-07 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_admin', '0006_alter_employee_telegram_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='telegram_user',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Телеграм-юзер'),
        ),
    ]
