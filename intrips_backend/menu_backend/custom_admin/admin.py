from django.contrib import admin
from .models import Order, Employee, Booking, Status, Task, InfoCard, AgreementCategory


class InfoCardAdmin(admin.ModelAdmin):
    list_display = ("id", "bold_text", "shop", "category")
    list_filter = ("shop", "category")
    search_fields = ("bold_text", "long_text")

    def save_model(self, request, obj, form, change):
        if not obj.shop_id:  # Если поле shop не установлено
            obj.shop = request.user.usersettings  # Привязываем к магазину пользователя
        obj.save()


admin.site.register(InfoCard, InfoCardAdmin)
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
