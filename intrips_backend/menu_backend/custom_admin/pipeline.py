from django.contrib.auth.models import User
from .models import PendingUser

def create_pending_user(strategy, details, response, user=None, *args, **kwargs):
    if user:
        return

    username = details.get('username') or details.get('first_name') + details.get('last_name')
    email = details.get('email')

    if not email:
        email = f"{username}@vk.com"

    user = User.objects.create_user(username=username, email=email)
    PendingUser.objects.create(user=user)
    return {'is_new': True}