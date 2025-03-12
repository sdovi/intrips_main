def set_unconfirmed(strategy, details, user=None, *args, **kwargs):
    """
    Устанавливает is_confirmed = False только для пользователей VK
    """
    if user and user.is_authenticated and user.is_superuser is False:
        user.is_confirmed = False
        user.save()
