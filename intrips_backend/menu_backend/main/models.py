from django.db import models
from django.contrib.auth.models import User

class UserSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="usersettings", verbose_name="Пользователь")
    name = models.CharField(max_length=255, unique=True, verbose_name="Название магазина")
    website_url = models.SlugField(unique=True, verbose_name="Уникальный URL")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    tg_bot_token = models.CharField(max_length=255, blank=True, null=True, verbose_name="Токен бота Telegram")
    tg_group_id = models.CharField(max_length=255, blank=True, null=True, verbose_name="ID группы Telegram")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Настройки магазина"
        verbose_name_plural = "Настройки магазинов"


class SubCategory(models.Model):
    user_settings = models.ForeignKey(UserSettings, on_delete=models.CASCADE, related_name='subcategories', verbose_name="Магазин")
    name = models.CharField(max_length=100, unique=True, verbose_name="Название категории")
    name_en = models.CharField(max_length=100, unique=True, blank=True, null=True, verbose_name="Название категории (En)")
    description = models.TextField(blank=True, verbose_name="Описание")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категории"
        verbose_name_plural = "Категории"


class Category(models.Model):
    user_settings = models.ForeignKey(UserSettings, on_delete=models.CASCADE, related_name='categories', verbose_name="Магазин")
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='items2', verbose_name="Подкатегория")
    name = models.CharField(max_length=100, unique=True, verbose_name="Название подкатегории")
    name_en = models.CharField(max_length=100, unique=True, blank=True, null=True, verbose_name="Название подкатегории (En)")
    description = models.TextField(blank=True, verbose_name="Описание")
    photo = models.ImageField(upload_to='category_photos/', blank=True, null=True, verbose_name="Фото")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Подкатегории"
        verbose_name_plural = "Подкатегории"


class MenuItem(models.Model):
    user_settings = models.ForeignKey(UserSettings, on_delete=models.CASCADE, related_name='menu_items', verbose_name="Магазин")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items', verbose_name="Категория")
    name = models.CharField(max_length=100, verbose_name="Название товара")
    name_en = models.CharField(max_length=100, blank=True, null=True, verbose_name="Название товара (En)")
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Цена")
    description = models.TextField(blank=True, verbose_name="Описание")
    description_en = models.TextField(blank=True, verbose_name="Описание (En)")
    photo = models.ImageField(upload_to='menu_photos/', blank=True, null=True, verbose_name="Фото")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Меню товаров"


class Headertext(models.Model):
    user_settings = models.ForeignKey(UserSettings, on_delete=models.CASCADE, related_name='header_texts', verbose_name="Магазин")
    name = models.CharField(max_length=100, verbose_name="Заголовок")
    name_en = models.CharField(max_length=100, blank=True, null=True, verbose_name="Заголовок (En)")
    photo = models.ImageField(upload_to='menu_photos/', blank=True, null=True, verbose_name="Фото")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Заголовочный текст"
        verbose_name_plural = "Заголовочные тексты"
