from django.db import models

from main.models import UserSettings  # Импортируем нашу модель магазина

class ChatMessage(models.Model):
    shop = models.ForeignKey(UserSettings, on_delete=models.CASCADE, related_name="messages")  # Привязка к магазину
    user_id = models.CharField(max_length=100)
    message = models.TextField()
    is_admin = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    replied_to = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{'Admin' if self.is_admin else 'User'} ({self.shop.website_url}): {self.message[:20]}"

