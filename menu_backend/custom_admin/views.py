from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views import View
from django.utils.timezone import now
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login
from django.contrib.auth.models import User
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
import requests
import json
import calendar
from datetime import datetime

from .models import Order, Booking, Employee, Status, Task
from .serializers import OrderSerializer, BookingSerializer, TaskSerializer
from .forms import EmployeeForm, BookingForm, TaskForm, AdminRegistrationForm, ConfirmOrderForm
from .statistics_service import ServiceStatistics
from django.views.decorators.csrf import csrf_exempt
from .serializers import EmployeeSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import AgreementCategory, InfoCard
from .serializers import AgreementCategorySerializer, InfoCardSerializer

# 🔹 Получение списка категорий и создание новой
@api_view(['GET', 'POST'])
def agreement_categories(request):
    if request.method == 'GET':
        categories = AgreementCategory.objects.all()
        serializer = AgreementCategorySerializer(categories, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = AgreementCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 🔹 Получение, обновление и удаление категории
@api_view(['GET', 'PUT', 'DELETE'])
def agreement_category_detail(request, category_id):
    try:
        category = AgreementCategory.objects.get(id=category_id)
    except AgreementCategory.DoesNotExist:
        return Response({'error': 'Категория не найдена'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AgreementCategorySerializer(category)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = AgreementCategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# 🔹 Получение списка карточек и создание новой
@api_view(['GET', 'POST'])
def info_cards(request):
    if request.method == 'GET':
        cards = InfoCard.objects.all()
        serializer = InfoCardSerializer(cards, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = InfoCardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 🔹 Получение, обновление и удаление карточки
@api_view(['GET', 'PUT', 'DELETE'])
def info_card_detail(request, card_id):
    try:
        card = InfoCard.objects.get(id=card_id)
    except InfoCard.DoesNotExist:
        return Response({'error': 'Карточка не найдена'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = InfoCardSerializer(card)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = InfoCardSerializer(card, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        card.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class EmployeeListView(generics.ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

API_URL = "https://intrips.site/api/bookings/"  # Замените на реальный URL API
def money_stats_view(request):
    # Получаем выбранный месяц
    selected_month = request.GET.get("month")

    # Русские названия месяцев
    months_list_ru = {
        1: "Январь", 2: "Февраль", 3: "Март",
        4: "Апрель", 5: "Май", 6: "Июнь",
        7: "Июль", 8: "Август", 9: "Сентябрь",
        10: "Октябрь", 11: "Ноябрь", 12: "Декабрь"
    }

    # Загружаем данные из API
    response = requests.get(API_URL)
    if response.status_code != 200:
        return JsonResponse({"error": "Ошибка загрузки данных"}, status=500)

    data = response.json()

    # Фильтруем только выполненные заказы (статус = 2)
    filtered_data = [entry for entry in data if entry["status"] == 2]

    # Фильтруем по месяцу, если он выбран
    if selected_month:
        filtered_data = [
            entry for entry in filtered_data
            if months_list_ru.get(datetime.strptime(entry["date"], "%Y-%m-%d").month) == selected_month
        ]

    # Группируем статистику по услугам и добавляем ₽
    stats = {}
    for entry in filtered_data:
        service_name = entry["service_name"]
        total_price = float(entry["total_price"])
        stats[service_name] = stats.get(service_name, 0) + total_price

    # Добавляем ₽ к значениям для Chart.js
    stats_with_currency = {k: f"{v:.2f} ₽" for k, v in stats.items()}

    context = {
        "filtered_data": filtered_data,
        "stats_json": json.dumps(stats_with_currency),  # Данные для Chart.js
        "months": months_list_ru.values(),  # Русские месяцы
        "selected_month": selected_month
    }
    
    return render(request, "custom_admin/money_stats.html", context)



def send_telegram_message(chat_id, text):
    """Отправка сообщения в Telegram"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Проверяем, нет ли ошибки при запросе
        return response.json()
    except requests.RequestException as e:
        print(f"Ошибка отправки сообщения в Telegram: {e}")
        return None

def confirm_order(request, order_id):
    """Подтверждение заказа: сохранение в бронирование + отправка уведомления"""
    order = get_object_or_404(Order, id=order_id)

    if request.method == "POST":
        employee_id = request.POST.get("employee")  # Получаем ID сотрудника из формы
        employee = get_object_or_404(Employee, id=employee_id)

        # Получаем название услуги из первого товара
        service_name = order.items[0]['name'] if order.items else "Неизвестная услуга"

        # Получаем статус "В работе"
        in_work_status = Status.objects.get_or_create(name="В работе")[0]

        # Создаём бронирование
        Booking.objects.create(
            service_name=service_name,
            room_number=order.room_number,
            guest_count=1,
            date=order.date,
            start_time=order.time,
            comment=order.comments,
            status=in_work_status,
            items=order.items,
            total_price=order.total_price,
            employee=employee
        )

        # Обновляем статус заказа
        order.status = "in_work"
        order.save()

        # ✅ Формируем сообщение для Telegram
        message_text = (
            f"📦 <b>Заказ №{order.id} подтверждён</b>\n"
            f"🏨 Комната: {order.room_number}\n"
            f"🛒 Товары:\n"
        )
        for item in order.items:
            message_text += f"  - {item['name']} (x{item['quantity']}) - {item['price']} ₽\n"

        message_text += f"\n💰 Общая сумма: {order.total_price} ₽\n"
        message_text += f"👷 Ответственный: {employee.full_name}"

        # ✅ Отправляем сообщение в Telegram (если у сотрудника есть user_id_tg)
        if employee.user_id_tg:
            send_telegram_message(employee.user_id_tg, message_text)
            messages.success(request, f"Заказ №{order.id} подтверждён, уведомление отправлено {employee.full_name}.")
        else:
            messages.error(request, f"У сотрудника {employee.full_name} нет Telegram ID!")

        return redirect(request.META.get("HTTP_REFERER", "/"))  # Возвращаем пользователя на ту же страницу

    return redirect("/")  # Если пришел GET-запрос, отправляем на главную





# Проверка, что пользователь - админ
def is_superuser(user):
    return user.is_authenticated and user.is_superuser

# Страница списка пользователей (только для админа)
@login_required(login_url="login")
@user_passes_test(is_superuser, login_url="dashboard")
def user_list(request):
    users = User.objects.filter(is_superuser=False)  # Показываем только обычных админов
    return render(request, "custom_admin/user_list.html", {"users": users})

# Удаление пользователя (AJAX)
@login_required(login_url="login")
@user_passes_test(is_superuser, login_url="dashboard")
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return JsonResponse({"success": True})
# Ограничение доступа только для админа
def is_superuser(user):
    return user.is_authenticated and user.is_superuser

# Вход только для зарегистрированных пользователей
@login_required(login_url="login")
def dashboard(request):
    new_orders_count = Order.objects.filter(status="new").count()
    return render(request, "custom_admin/base.html", {"new_orders_count": new_orders_count})

# Администратор регистрирует новых пользователей
@login_required(login_url="login")
@user_passes_test(is_superuser, login_url="dashboard")  
def register_admin(request):
    if request.method == "POST":
        form = AdminRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.is_staff = True  # Даем права администратора
            user.save()
            return redirect("dashboard")
    else:
        form = AdminRegistrationForm()

    return render(request, "custom_admin/register.html", {"form": form})






def purchase_stats_view(request):
    service_statistics = ServiceStatistics()
    filtered_data = service_statistics.filter_data()
    stats = service_statistics.get_statistics()

    # Преобразуем статистику в JSON для передачи в JavaScript
    context = {
        "bookings": filtered_data,
        "stats_json": json.dumps(stats)  # Безопасная передача данных для Chart.js
    }
    return render(request, 'custom_admin/purchase_stats.html', context)


@api_view(['GET', 'POST'])
def bookings(request):
    if request.method == 'GET':
        bookings = Booking.objects.all()
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Токен бота (ОСТОРОЖНО, лучше хранить его в настройках!)
TELEGRAM_BOT_TOKEN = "7222921497:AAHdC-9gxrjaTHlItXjkZafA_7ldGVuPwTE"

def send_message(request, employee_id):
    """Форма для ввода сообщения"""
    employee = get_object_or_404(Employee, id=employee_id)

    if request.method == "POST":
        message_text = request.POST.get("message", "").strip()
        if message_text:
            return redirect('send_message_process', employee_id=employee.id)

    return render(request, "custom_admin/send_message.html", {"employee": employee})


def send_message_process(request, employee_id):
    """Отправляет сообщение через Telegram бота"""
    employee = get_object_or_404(Employee, id=employee_id)

    if request.method == "POST":
        message_text = request.POST.get("message", "").strip()
        
        if not message_text:
            messages.error(request, "Сообщение не может быть пустым!")
            return redirect('send_message', employee_id=employee.id)

        if not employee.user_id_tg:
            messages.error(request, "У сотрудника нет Telegram ID!")
            return redirect('send_message', employee_id=employee.id)

        # Telegram API URL
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {
            "chat_id": employee.user_id_tg,  # ID пользователя в Telegram
            "text": message_text,
            "parse_mode": "HTML"  # Можно использовать HTML-разметку
        }

        try:
            response = requests.post(url, json=data)
            response_data = response.json()

            if response.status_code == 200 and response_data.get("ok"):
                messages.success(request, "Сообщение успешно отправлено!")
            else:
                messages.error(request, f"Ошибка отправки: {response_data.get('description', 'Неизвестная ошибка')}")
        
        except requests.RequestException as e:
            messages.error(request, f"Ошибка соединения: {e}")

    return redirect('send_message', employee_id=employee.id)

@api_view(['GET'])
def task_list_api(request):
    tasks = Task.objects.all()
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)




class TaskCalendarView(View):
    def get(self, request):
        return render(request, "custom_admin/order_calendar.html")

def task_events(request):
    tasks = Task.objects.all()
    events = [
        {
            "title": task.description,
            "start": f"{task.date}T{task.time}",
            "color": "#"+task.employee.id.__str__()[:6]  # Генерация цвета
        } for task in tasks
    ]
    return JsonResponse(events, safe=False)

# 📌 Список задач + Фильтрация
def task_list(request):
    tasks = Task.objects.all()
    
    # Фильтрация
    date_filter = request.GET.get('date', None)
    room_filter = request.GET.get('room', None)
    if date_filter:
        tasks = tasks.filter(date=date_filter)
    if room_filter:
        tasks = tasks.filter(room=room_filter)

    return render(request, 'custom_admin/apps.html', {'tasks': tasks})

# 📌 Добавление задачи
def add_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()
        
    employees = Employee.objects.all()  # Получаем всех сотрудников
    return render(request, 'custom_admin/task_form.html', {'form': form, 'employees': employees})

def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)

    employees = Employee.objects.all()  # 👈 Передаём сотрудников
    return render(request, 'custom_admin/task_form.html', {'form': form, 'employees': employees})



# 📌 Удаление задачи
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == "POST":
        task.delete()
        return redirect('task_list')
    return render(request, 'custom_admin/task_confirm_delete.html', {'task': task})



@csrf_exempt  # Если используешь CSRF-токен в шаблоне, эту строку можно убрать
def update_booking_status(request, booking_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Получаем данные из fetch()
            status_id = data.get("status_id")

            booking = get_object_or_404(Booking, id=booking_id)
            new_status = get_object_or_404(Status, id=status_id)

            booking.status = new_status
            booking.save()

            return JsonResponse({"success": True, "status": new_status.name})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    
    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)

def booking_create(request):
    """Создание бронирования с отправкой уведомления в Telegram"""
    # Получаем список услуг из API
    try:
        services = requests.get("https://intrips.site/api/categories/").json()  # Актуальный API
    except requests.exceptions.RequestException:
        services = []

    employees = Employee.objects.all()
    statuses = Status.objects.all()

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)  # Сохраняем без коммита
            
            # Назначаем статус бронирования
            booking.status = Status.objects.get(id=request.POST.get("status"))
            booking.save()  # Теперь сохраняем в БД
            
            # Отправка уведомления в Telegram, если выбран сотрудник
            employee_id = request.POST.get("employee")
            if employee_id:
                employee = get_object_or_404(Employee, id=employee_id)

                if employee.user_id_tg:
                    # Формируем текст сообщения
                    message_text = (
                        f"🔔 <b>Новое бронирование услуги</b>\n"
                        f"🏷 Услуга: {booking.service_name}\n"
                        f"📅 Дата: {booking.date}\n"
                        f"⏰ Время: {booking.start_time} - {booking.end_time}\n"
                        f"🚪 Комната: {booking.room_number}\n"
                        f"👥 Количество гостей: {booking.guest_count}\n"
                        f"📝 Комментарий: {booking.comment or 'Нет'}"
                    )

                    # Отправляем сообщение в Telegram
                    send_telegram_message(employee.user_id_tg, message_text)
                else:
                    messages.warning(request, "Сотрудник не имеет Telegram ID, уведомление не отправлено.")

            messages.success(request, "Бронирование успешно создано!")
            return redirect('bookings_list')
        else:
            print("Ошибки формы:", form.errors)

    else:
        form = BookingForm()

    return render(request, 'custom_admin/booking_form.html', {
        'form': form,
        'services': services,
        'employees': employees,
        'statuses': statuses,
    })

def bookings_list(request):
    in_progress_status = Status.objects.get(name="В работе")  # Получаем статус "В работе"
    bookings = Booking.objects.filter(status=in_progress_status)  # Фильтруем бронирования
    statuses = Status.objects.all()
    
    return render(request, 'custom_admin/bookings.html', {'bookings': bookings, 'statuses': statuses})


def archive_list(request):
    archive_statuses = Status.objects.filter(name__in=["Отменен", "Выполнено"])
    archived_bookings = Booking.objects.filter(status__in=archive_statuses)
    statuses = Status.objects.all()  # ⚡ ДОБАВИЛ `statuses`, иначе кнопки работать не будут!

    return render(request, 'custom_admin/archive.html', {'bookings': archived_bookings, 'statuses': statuses})

def employees(request):
    employees = Employee.objects.all()  # Получаем всех сотрудников
    return render(request, "custom_admin/employees.html", {"employees": employees})  





def employees_list(request):
    employees = Employee.objects.all()  # Получаем всех сотрудников
    
    print("Сотрудники:", employees)  # Выведет список в консоли Django
    return render(request, 'custom_admin/employees.html', {'employees': employees})

def employee_create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employees_list')
    else:
        form = EmployeeForm()
    return render(request, 'custom_admin/employee_form.html', {'form': form})

def employee_edit(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employees_list')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'custom_admin/employee_form.html', {'form': form})

def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        employee.delete()
        return redirect('employees_list')
    return render(request, 'custom_admin/employee_confirm_delete.html', {'employee': employee})







class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all().order_by("-created_at")  # Новые заказы в начале
    serializer_class = OrderSerializer


# def dashboard(request):
#     return render(request, "custom_admin/base.html")




def chat_guest(request):
    return render(request, "custom_admin/chat_guest.html")




def apps(request):
    return render(request, "custom_admin/apps.html")




def services(request):
    return render(request, "custom_admin/services.html")






def order_calendar(request):
    return render(request, "custom_admin/order_calendar.html")

def get_tasks(request):
    """API для передачи событий в календарь"""
    tasks = Task.objects.all()
    events = [
        {
            "title": task.description,  # Название события
            "start": f"{task.date}T{task.time}",  # Дата и время в ISO-формате
            "color": "blue"  # Цвет можно менять по логике
        }
        for task in tasks
    ]
    return JsonResponse(events, safe=False)


def employees(request):
    employees = Employee.objects.all()  # Получаем всех сотрудников
    return render(request, "custom_admin/employees.html", {"employees": employees})  




def purchase_stats(request):
    return render(request, "custom_admin/purchase_stats.html")


def orders(request):
    orders = Order.objects.all().order_by("-status", "-created_at")
    employees = Employee.objects.all()
    new_orders_count = Order.objects.filter(status="new").count()  # Считаем заявки
    return render(request, "custom_admin/orders.html", {
        "orders": orders, 
        "employees": employees, 
        "new_orders_count": new_orders_count  # Передаем в шаблон
    })