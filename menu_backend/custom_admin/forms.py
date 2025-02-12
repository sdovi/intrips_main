from django import forms
from .models import Employee, Booking

from .models import Task

from django import forms
from .models import Task


from django import forms
from django.contrib.auth.models import User

from django import forms
from .models import Employee

class ConfirmOrderForm(forms.Form):
    employee = forms.ModelChoiceField(
        queryset=Employee.objects.all(),
        label="Выберите сотрудника",
        empty_label="Выберите сотрудника",
        widget=forms.Select(attrs={'class': 'form-control'})
    )










class AdminRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Подтверждение пароля")

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Пароли не совпадают!")

        return cleaned_data

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['description', 'room', 'date', 'time', 'end_time', 'employee']  # 👈 end_time включено
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),  # 👈 Добавлено end_time
        }

from django import forms
from .models import Employee

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'
        widgets = {
            'color': forms.Select(attrs={'class': 'form-control'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите ФИО'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите номер телефона'}),
            # 'telegram_user': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите телеграм-юзер'}),
            'position': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите должность'}),
            'user_id_tg': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Введите Telegram ID'}),
        }

# class EmployeeForm(forms.ModelForm):
#     class Meta:
#         model = Employee
#         fields = '__all__'
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def clean_total_price(self):
        total_price = self.cleaned_data.get("total_price")
        return total_price or 0.00  # Устанавливаем 0.00, если поле пустое

    def clean_items(self):
        items = self.cleaned_data.get("items")
        return items or {}  # Устанавливаем пустой словарь, если ничего нет
