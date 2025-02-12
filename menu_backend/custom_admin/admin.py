from django.contrib import admin
from .models import Order

from .models import Employee, Booking, Status, Task,InfoCard,AgreementCategory

admin.site.register(InfoCard, admin.ModelAdmin)
admin.site.register(AgreementCategory, admin.ModelAdmin)

admin.site.register(Employee, admin.ModelAdmin)
admin.site.register(Booking, admin.ModelAdmin)
admin.site.register(Status, admin.ModelAdmin)

admin.site.register(Task, admin.ModelAdmin)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "total_price", "date", "time", "room_number", "status", "created_at")
    list_filter = ("status", "date")
    search_fields = ("room_number", "comments")

