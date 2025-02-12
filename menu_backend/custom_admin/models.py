from django.db import models

class AgreementCategory(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название категории")

    def __str__(self):
        return "пользовательское соглашение"

class InfoCard(models.Model):
    category = models.ForeignKey(AgreementCategory, on_delete=models.CASCADE, related_name="info_cards", verbose_name="Категория")
    image = models.ImageField(upload_to="menu_photos/", verbose_name="Фото")
    bold_text = models.CharField(max_length=255, verbose_name="Текст жирный")
    long_text = models.TextField(verbose_name="Длинный текст")
    bold_text_en = models.CharField(max_length=255, verbose_name="Текст жирный (En)")
    long_text_en = models.TextField(verbose_name="Длинный текст (En)")

    def __str__(self):
        return "Карточки пользовательского соглашение"



class Task(models.Model):
    description = models.TextField(verbose_name="Описание")
    room = models.CharField(max_length=10, verbose_name="Номер комнаты")
    date = models.DateField(verbose_name="Дата")
    time = models.TimeField(verbose_name="Начало")
    end_time = models.TimeField(verbose_name="Конец", null=True, blank=True)  # Добавляем конец времени
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE, verbose_name="Ответственный сотрудник")

    def __str__(self):
        return f"{self.description} - {self.room} - {self.date} ({self.time} - {self.end_time})"




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
    # telegram_user = models.CharField(
    #     max_length=100, verbose_name="Телеграм-юзер", blank=True, null=True
    # )  
    position = models.CharField(max_length=255, verbose_name="Должность")
    user_id_tg = models.BigIntegerField(verbose_name="Telegram ID", unique=True, null=True, blank=True)

    
    def __str__(self):
        return self.full_name


        

class Status(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название статуса")

    def __str__(self):
        return self.name


class Booking(models.Model):
    service_name = models.CharField(max_length=255, verbose_name="Название услуги")
    room_number = models.CharField(max_length=10, verbose_name="Номер комнаты")
    guest_count = models.PositiveIntegerField(verbose_name="Количество человек", default=1)
    date = models.DateField(verbose_name="Дата бронирования")
    start_time = models.TimeField(verbose_name="Время начала")
    end_time = models.TimeField(verbose_name="Время окончания", null=True, blank=True)
    employee = models.ForeignKey('Employee', on_delete=models.SET_NULL, null=True, verbose_name="Сотрудник")
    comment = models.TextField(blank=True, verbose_name="Комментарий")
    status = models.ForeignKey('Status', on_delete=models.SET_NULL, null=True, verbose_name="Статус")

    # Новые поля
    items = models.JSONField(verbose_name="Товары", default=dict, null=True, blank=True)  # JSON-массив товаров
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Общая сумма", null=True, blank=True)

    def __str__(self):
        return f"{self.service_name} - {self.date}"

class Order(models.Model):
    items = models.JSONField()  # JSON-массив товаров [{name: "Item 1", quantity: 2, price: 500}]
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    time = models.TimeField()
    room_number = models.CharField(max_length=10)  # Номер комнаты
    comments = models.TextField(blank=True)  # Комментарии клиента
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания

    STATUS_CHOICES = [
        ("new", "Новый"),
        ("processing", "В обработке"),
        ("completed", "Завершен"),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")

    def __str__(self):
        return f"Заказ {self.id} на {self.total_price} ₽ - {self.get_status_display()}"
