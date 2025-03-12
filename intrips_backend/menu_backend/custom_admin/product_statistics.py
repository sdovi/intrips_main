from datetime import datetime
from .models import Booking

class ServiceStatistics:
    STATUS_MAPPING = {
        1: "В работе",
        2: "Выполнен",
        3: "Отменен"
    }

    def __init__(self, shop):
        """Инициализация статистики для конкретного магазина"""
        self.bookings = Booking.objects.filter(shop=shop)

    def filter_data(self, start_date=None, end_date=None):
        """Фильтруем бронирования по датам"""
        filtered_data = []
        for booking in self.bookings:
            booking_date = booking.date
            if (not start_date or booking_date >= start_date) and \
               (not end_date or booking_date <= end_date):
                booking.status_text = self.STATUS_MAPPING.get(booking.status.id, "Неизвестно")
                filtered_data.append(booking)
        return filtered_data

    def get_statistics(self):
        """Получаем количество бронирований по статусу"""
        stats = {"В работе": 0, "Выполнен": 0, "Отменен": 0}
        for booking in self.bookings:
            status_text = self.STATUS_MAPPING.get(booking.status.id, "Неизвестно")
            stats[status_text] += 1
        return stats
