import requests
from datetime import datetime

class ServiceStatistics:
    API_URL = "https://intrips.site/api/bookings/"
    
    STATUS_MAPPING = {
        1: "В работе",
        2: "Выполнен",
        3: "Отменен"
    }

    def __init__(self):
        self.bookings = self._fetch_data()

    def _fetch_data(self):
        try:
            response = requests.get(self.API_URL)
            response.raise_for_status()
            return response.json()
        except requests.RequestException:
            return []

    def filter_data(self, start_date=None, end_date=None):
        filtered_data = []
        for booking in self.bookings:
            booking_date = datetime.strptime(booking['date'], '%Y-%m-%d')
            if (not start_date or booking_date >= start_date) and \
               (not end_date or booking_date <= end_date):
                booking["status_text"] = self.STATUS_MAPPING.get(booking["status"], "Неизвестно")
                filtered_data.append(booking)
        return filtered_data

    def get_statistics(self):
        stats = {"В работе": 0, "Выполнен": 0, "Отменен": 0}
        for booking in self.bookings:
            status_text = self.STATUS_MAPPING.get(booking["status"], "Неизвестно")
            stats[status_text] += 1
        return stats
