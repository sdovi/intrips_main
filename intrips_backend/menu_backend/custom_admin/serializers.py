from rest_framework import serializers
from .models import Order

from .models import Task
from .models import Booking
from .models import Employee
from .models import AgreementCategory, InfoCard

class AgreementCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AgreementCategory
        fields = "__all__"

class InfoCardSerializer(serializers.ModelSerializer):
    category = AgreementCategorySerializer()

    class Meta:
        model = InfoCard
        fields = "__all__"

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'color', 'full_name', 'phone_number', 'position', 'user_id_tg']

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'  # Можно указать конкретные поля, если нужно
        
        
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
