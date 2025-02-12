from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.conf import settings

class Command(BaseCommand):
    help = "Создает главного администратора, если он отсутствует"

    def handle(self, *args, **kwargs):
        admin_data = settings.ADMIN_CREDENTIALS
        username = admin_data["username"]
        password = admin_data["password"]

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, password=password)
            self.stdout.write(self.style.SUCCESS(f"Администратор {username} создан!"))
        else:
            self.stdout.write(self.style.WARNING(f"Администратор {username} уже существует."))
