from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now
from main.models import UserSettings  # Импортируем нашу модель магазина
from main.models import UserSettings  # Импорт UserSettings до Employee


class AgreementCategory(models.Model):
    shop = models.ForeignKey(UserSettings, on_delete=models.CASCADE, verbose_name="Магазин")
    title = models.CharField(max_length=255, verbose_name="Название категории")

    def __str__(self):
        return f"Категория ({self.title}) - {self.shop}"

    class Meta:
        verbose_name = "Категория соглашения"
        verbose_name_plural = "Категории соглашений"


class InfoCard(models.Model):
    shop = models.ForeignKey(UserSettings, on_delete=models.CASCADE, verbose_name="Магазин")
    category = models.ForeignKey(AgreementCategory, on_delete=models.CASCADE, related_name="info_cards", verbose_name="Категория")
    image = models.ImageField(upload_to="menu_photos/", verbose_name="Фото")
    bold_text = models.CharField(max_length=255, verbose_name="Текст жирный")
    long_text = models.TextField(verbose_name="Длинный текст")
    bold_text_en = models.CharField(max_length=255, verbose_name="Текст жирный (En)")
    long_text_en = models.TextField(verbose_name="Длинный текст (En)")

    def __str__(self):
        return f"Карточка ({self.bold_text}) - {self.shop}"

    class Meta:
        verbose_name = "Пользовательское соглашение карточка"
        verbose_name_plural = "Пользовательское соглашение карточки"



class Task(models.Model):
    shop = models.ForeignKey(UserSettings, on_delete=models.CASCADE, verbose_name="Магазин")
    description = models.TextField(verbose_name="Описание")
    room = models.CharField(max_length=10, verbose_name="Номер комнаты")
    date = models.DateField(verbose_name="Дата")
    time = models.TimeField(verbose_name="Начало")
    end_time = models.TimeField(verbose_name="Конец", null=True, blank=True)
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE, verbose_name="Ответственный сотрудник")

    def __str__(self):
        return f"{self.description} - {self.room} - {self.date} ({self.time} - {self.end_time})"

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"


class Employee(models.Model):
    COLOR_CHOICES = [
        ('red', 'Красный'),
        ('blue', 'Синий'),
        ('green', 'Зеленый'),
        ('yellow', 'Желтый'),
    ]

    color = models.CharField(max_length=20, choices=COLOR_CHOICES, verbose_name="Цвет")
    full_name = models.CharField(max_length=255, verbose_name="ФИО")
    phone_number = models.CharField(max_length=20, verbose_name="Номер телефона")
    position = models.CharField(max_length=255, verbose_name="Должность")
    user_id_tg = models.BigIntegerField(verbose_name="Telegram ID", unique=True, null=True, blank=True)
    shop = models.ForeignKey(UserSettings, on_delete=models.CASCADE, verbose_name="Магазин")

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"


class Status(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название статуса")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"


class Booking(models.Model):
    shop = models.ForeignKey(UserSettings, on_delete=models.CASCADE, verbose_name="Магазин")
    service_name = models.CharField(max_length=255, verbose_name="Название услуги")
    room_number = models.CharField(max_length=10, verbose_name="Номер комнаты")
    guest_count = models.PositiveIntegerField(verbose_name="Количество человек", default=1)
    date = models.DateField(verbose_name="Дата бронирования")
    start_time = models.TimeField(verbose_name="Время начала")
    end_time = models.TimeField(verbose_name="Время окончания", null=True, blank=True)
    employee = models.ForeignKey('Employee', on_delete=models.SET_NULL, null=True, verbose_name="Сотрудник")
    comment = models.TextField(blank=True, verbose_name="Комментарий")
    status = models.ForeignKey('Status', on_delete=models.SET_NULL, null=True, verbose_name="Статус")
    items = models.JSONField(verbose_name="Товары", default=dict, null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Общая сумма", null=True, blank=True)

    def __str__(self):
        return f"{self.service_name} - {self.date}"

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"


class Order(models.Model):
    shop = models.ForeignKey(UserSettings, on_delete=models.CASCADE, related_name="orders", verbose_name="Магазин")
    items = models.JSONField(verbose_name="Товары")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Общая сумма")
    date = models.DateField(verbose_name="Дата")
    time = models.TimeField(verbose_name="Время")
    room_number = models.CharField(max_length=10, verbose_name="Номер комнаты")
    comments = models.TextField(blank=True, verbose_name="Комментарии")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    
    STATUS_CHOICES = [
        ("new", "Новый"),
        ("processing", "В обработке"),
        ("completed", "Завершен"),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new", verbose_name="Статус")

    def __str__(self):
        return f"Заказ {self.id} на {self.total_price} ₽ - {self.get_status_display()}"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
