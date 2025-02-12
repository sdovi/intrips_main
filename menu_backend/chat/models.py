from django.db import models


class ChatMessage(models.Model):
    user_id = models.CharField(max_length=100)
    message = models.TextField()
    is_admin = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    replied_to = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{'Admin' if self.is_admin else 'User'}: {self.message[:20]}"
