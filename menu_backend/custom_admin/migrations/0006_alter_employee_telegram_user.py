# Generated by Django 5.1.5 on 2025-02-07 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_admin', '0005_employee_user_id_tg'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='telegram_user',
            field=models.CharField(max_length=100, null=True, verbose_name='Телеграм-юзер'),
        ),
    ]
