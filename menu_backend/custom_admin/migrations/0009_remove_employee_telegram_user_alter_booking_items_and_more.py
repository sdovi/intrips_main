# Generated by Django 5.1.5 on 2025-02-07 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_admin', '0008_alter_employee_telegram_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='telegram_user',
        ),
        migrations.AlterField(
            model_name='booking',
            name='items',
            field=models.JSONField(blank=True, default=dict, null=True, verbose_name='Товары'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='total_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Общая сумма'),
        ),
    ]
