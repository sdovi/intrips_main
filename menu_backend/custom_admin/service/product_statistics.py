import requests
import json
from collections import defaultdict

API_URL = "https://intrips.site/api/bookings/"
COMPLETED_STATUS = 2  # Статус завершенного заказа


class ProductStatistics:
    def __init__(self):
        self.data = self._fetch_data()

    def _fetch_data(self):
        """Запрашиваем данные по API."""
        try:
            response = requests.get(API_URL)
            response.raise_for_status()
            return response.json()
        except requests.RequestException:
            return []  # В случае ошибки возвращаем пустой список

    def filter_completed_orders(self):
        """Фильтруем заказы только со статусом COMPLETED_STATUS (2)."""
        return [booking for booking in self.data if booking["status"] == COMPLETED_STATUS]

    def get_statistics(self):
        """Подсчитываем количество покупок и сумму продаж по каждому товару."""
        product_stats = defaultdict(lambda: {"total_quantity": 0, "total_sales": 0})

        for booking in self.filter_completed_orders():
            for item in booking.get("items", []):
                name = item["name"]
                quantity = item["quantity"]
                total_price = item["quantity"] * item["price"]

                product_stats[name]["total_quantity"] += quantity
                product_stats[name]["total_sales"] += total_price

        return product_stats
