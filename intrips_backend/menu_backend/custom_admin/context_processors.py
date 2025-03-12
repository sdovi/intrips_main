from .models import Order

def new_orders_count(request):
    if hasattr(request.user, 'usersettings'):
        shop = request.user.usersettings
        new_orders_count = Order.objects.filter(status="new", shop__website_url=shop.website_url).count()
        return {
            "new_orders_count": new_orders_count,
            "shop": shop
        }
    return {}
