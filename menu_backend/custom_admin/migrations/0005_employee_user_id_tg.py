# Generated by Django 5.1.5 on 2025-02-06 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_admin', '0004_booking_items_booking_total_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='user_id_tg',
            field=models.BigIntegerField(blank=True, null=True, unique=True, verbose_name='Telegram ID'),
        ),
    ]
