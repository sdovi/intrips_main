from django.db import models


class SubCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    name_en = models.CharField(max_length=100, unique=True, blank=True, null=True)  # Английская версия названия
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='items2')
    name = models.CharField(max_length=100, unique=True)
    name_en = models.CharField(max_length=100, unique=True, blank=True, null=True)  # Английская версия названия
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to='category_photos/', blank=True, null=True)  # Поле для фото

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100, blank=True, null=True)  # Английская версия названия
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField(blank=True)
    description_en = models.TextField(blank=True)
    photo = models.ImageField(upload_to='menu_photos/', blank=True, null=True)

    def __str__(self):
        return self.name


class Headertext(models.Model):
    name = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100, blank=True, null=True)  # Английская версия текста
    photo = models.ImageField(upload_to='menu_photos/', blank=True, null=True)

    def __str__(self):
        return self.name
