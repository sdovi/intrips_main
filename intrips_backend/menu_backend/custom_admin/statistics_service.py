from datetime import datetime
from .models import Booking

class ServiceStatistics:
    VALID_STATUSES = {"В работе", "Выполнено", "Отменен"}  # Названия статусов

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
                booking.status_text = booking.status.name if booking.status and booking.status.name in self.VALID_STATUSES else "Неизвестно"
                filtered_data.append(booking)
        return filtered_data

    def get_statistics(self):
        """Получаем количество бронирований по статусу"""
        stats = {status: 0 for status in self.VALID_STATUSES}  # Инициализируем счетчики

        for booking in self.bookings:
            if booking.status and booking.status.name in self.VALID_STATUSES:
                stats[booking.status.name] += 1  # Увеличиваем счетчик по названию

        return stats
