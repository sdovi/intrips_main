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
from django.http import HttpResponse
from datetime import datetime

from .forms import ShopForm
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
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
import json


from django.shortcuts import render, redirect
from .forms import CreateShopForm
from django.shortcuts import render, get_object_or_404
from main.models import UserSettings

def custom_admin_dashboard(request, shop_url):
    shop = get_object_or_404(UserSettings, website_url=shop_url)
    return render(request, 'custom_admin/dashboard.html', {'shop': shop})





@login_required(login_url="login")
def create_shop(request):
    """Создаёт магазин для пользователя"""
    if hasattr(request.user, 'usersettings'):
        return redirect("dashboard")  # Если магазин уже есть, отправляем в админку

    if request.method == "POST":
        name = request.POST.get("name", "").strip()  # Убираем пробелы в начале и конце
        website_url = request.POST.get("website_url", "").strip()

        # Проверяем, заполнены ли все поля
        if not name or not website_url:
            return render(request, "custom_admin/create_shop.html", {"error": "Все поля обязательны!"})

        # Проверяем, не занят ли URL
        if UserSettings.objects.filter(website_url=website_url).exists():
            return render(request, "custom_admin/create_shop.html", {"error": "Этот URL уже занят!"})

        # Создаём магазин
        shop = UserSettings.objects.create(user=request.user, name=name, website_url=website_url)

        return redirect("dashboard")

    return render(request, "custom_admin/create_shop.html")



# 🔹 Получение списка категорий и создание новой

# 🔹 Получение списка категорий и создание новой
@api_view(['GET', 'POST'])
def agreement_categories(request, shop_url=None):
    # Фильтрация категорий по shop_url
    if shop_url:
        try:
            shop = UserSettings.objects.get(website_url=shop_url)
            categories = AgreementCategory.objects.filter(shop=shop)
        except UserSettings.DoesNotExist:
            return Response({'error': 'Магазин не найден'}, status=status.HTTP_404_NOT_FOUND)
    else:
        categories = AgreementCategory.objects.all()

    # Сериализация данных
    serializer = AgreementCategorySerializer(categories, many=True)
    return Response(serializer.data)

# 🔹 Получение, обновление и удаление категории
@api_view(['GET', 'PUT', 'DELETE'])
def agreement_category_detail(request, category_id, shop_url=None):
    try:
        # Если передан shop_url, фильтруем по магазину
        if shop_url:
            shop = UserSettings.objects.get(website_url=shop_url)
            category = AgreementCategory.objects.get(id=category_id, shop=shop)
        else:
            category = AgreementCategory.objects.get(id=category_id)

    except (AgreementCategory.DoesNotExist, UserSettings.DoesNotExist):
        return Response({'error': 'Категория или магазин не найдены'}, status=status.HTTP_404_NOT_FOUND)

    # Обработка запросов для категории
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
def info_cards(request, shop_url=None):
    if shop_url:
        try:
            shop = UserSettings.objects.get(website_url=shop_url)
            cards = InfoCard.objects.filter(shop=shop)
        except UserSettings.DoesNotExist:
            return Response({'error': 'Магазин не найден'}, status=status.HTTP_404_NOT_FOUND)
    else:
        cards = InfoCard.objects.all()

    # Сериализация данных
    serializer = InfoCardSerializer(cards, many=True)
    return Response(serializer.data)

# 🔹 Получение, обновление и удаление карточки
@api_view(['GET', 'PUT', 'DELETE'])
def info_card_detail(request, card_id, shop_url=None):
    try:
        # Если передан shop_url, фильтруем по магазину
        if shop_url:
            shop = UserSettings.objects.get(website_url=shop_url)
            card = InfoCard.objects.get(id=card_id, shop=shop)
        else:
            card = InfoCard.objects.get(id=card_id)

    except (InfoCard.DoesNotExist, UserSettings.DoesNotExist):
        return Response({'error': 'Карточка или магазин не найдены'}, status=status.HTTP_404_NOT_FOUND)

    # Обработка запросов для карточки
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
from django.shortcuts import render, get_object_or_404
from custom_admin.models import Booking, UserSettings, Status
import json
from datetime import datetime

def money_stats_view(request, shop_url):
    """Статистика по деньгам для конкретного магазина"""

    # Получаем магазин или выдаем 404, если его нет
    shop = get_object_or_404(UserSettings, website_url=shop_url)

    # Получаем статус "Выполнено", но если его нет — просто ставим None
    completed_status = Status.objects.filter(name="Выполнено").first()

    # Если статуса нет, просто создаём пустой список бронирований
    if completed_status:
        bookings_done = Booking.objects.filter(shop=shop, status=completed_status)
    else:
        bookings_done = []

    # Русские названия месяцев
    months_list_ru = {
        1: "Январь", 2: "Февраль", 3: "Март",
        4: "Апрель", 5: "Май", 6: "Июнь",
        7: "Июль", 8: "Август", 9: "Сентябрь",
        10: "Октябрь", 11: "Ноябрь", 12: "Декабрь"
    }

    # Фильтрация по месяцу
    selected_month = request.GET.get("month")
    if selected_month:
        bookings_done = [
            booking for booking in bookings_done
            if months_list_ru.get(booking.date.month) == selected_month
        ]

    # Группируем статистику по услугам
    stats = {}
    for booking in bookings_done:
        service_name = booking.service_name
        total_price = float(booking.total_price) if booking.total_price else 0
        stats[service_name] = stats.get(service_name, 0) + total_price

    # Форматируем суммы в ₽
    stats_with_currency = {k: f"{v:.2f} ₽" for k, v in stats.items()}

    context = {
        
        "shop": shop,  # Добавляем объект магазина
        "filtered_data": bookings_done,
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

def confirm_order(request, shop_url, order_id):
    """Подтверждение заказа с учетом магазинов + отправка уведомления"""
    shop = get_object_or_404(UserSettings, website_url=shop_url)
    order = get_object_or_404(Order, id=order_id, shop=shop)

    if request.method == "POST":
        employee_id = request.POST.get("employee")
        employee = get_object_or_404(Employee, id=employee_id)

        service_name = order.items[0]["name"] if order.items else "Неизвестная услуга"
        in_work_status = Status.objects.get_or_create(name="В работе")[0]

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
            employee=employee,
            shop=shop,
        )

        order.status = "in_work"
        order.employee = employee
        order.save()

        message_text = (
            f"📦 <b>Заказ №{order.id} подтверждён</b>\n"
            f"🏨 Комната: {order.room_number}\n"
            f"🛒 Товары:\n"
        )

        for item in order.items:
            message_text += f"  - {item['name']} (x{item['quantity']}) - {item['price']} ₽\n"

        message_text += f"\n💰 Общая сумма: {order.total_price} ₽\n"
        message_text += f"👷 Ответственный: {employee.full_name}"

        if employee.user_id_tg:
            send_telegram_message(employee.user_id_tg, message_text)
            messages.success(request, f"Заказ №{order.id} подтверждён, уведомление отправлено {employee.full_name}.")
        else:
            messages.error(request, f"У сотрудника {employee.full_name} нет Telegram ID!")

        return redirect(request.META.get("HTTP_REFERER", "/"))

    return redirect("/")








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


@login_required(login_url="login")
def edit_shop(request, shop_url):
    """Редактирование магазина по URL"""
    shop = get_object_or_404(UserSettings, website_url=shop_url)

    # Проверяем, имеет ли пользователь доступ к магазину
    if shop.user != request.user:
        return redirect("dashboard")  # Перенаправляем, если нет доступа

    if request.method == "POST":
        form = ShopForm(request.POST, instance=shop)
        if form.is_valid():
            form.save()
            return redirect("dashboard")  # Возвращаемся в панель управления

    else:
        form = ShopForm(instance=shop)

    return render(request, "custom_admin/edit_shop.html", {"form": form, "shop": shop})





@login_required(login_url="login")
def get_new_orders_count(request):
    if hasattr(request.user, 'usersettings'):
        shop = request.user.usersettings
        new_orders_count = Order.objects.filter(status="new", shop__website_url=shop.website_url).count()
        return JsonResponse({"new_orders_count": new_orders_count})
    return JsonResponse({"new_orders_count": 0})

@login_required(login_url="login")
def dashboard(request):
    if hasattr(request.user, "usersettings"):
        shop = request.user.usersettings
        new_orders_count = Order.objects.filter(status="new", shop__website_url=shop.website_url).count()

        return render(request, "custom_admin/base.html", {
            "shop": shop,
            "new_orders_count": new_orders_count,
        })
    return redirect("create_shop")




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
            return redirect("user_list")
    else:
        form = AdminRegistrationForm()

    return render(request, "custom_admin/register.html", {"form": form})





def purchase_stats_view(request, shop_url):
    shop = get_object_or_404(UserSettings, website_url=shop_url)  # Получаем магазин
    service_statistics = ServiceStatistics(shop)  # Передаём в статистику магазин
    filtered_data = service_statistics.filter_data()  # Фильтруем данные
    stats = service_statistics.get_statistics()  # Получаем статистику

    context = {
        "bookings": filtered_data,
        "stats_json": json.dumps(stats),  # Передаём данные в JavaScript
        "shop": shop
    }
    return render(request, 'custom_admin/purchase_stats.html', context)

@api_view(['GET', 'POST'])
def bookings(request, shop_url):
    """Возвращает список бронирований для конкретного магазина"""
    
    # Проверяем, существует ли магазин
    shop = get_object_or_404(UserSettings, website_url=shop_url)
    
    if request.method == 'GET':
        # Фильтруем бронирования по магазину
        bookings = Booking.objects.filter(shop=shop)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # Добавляем магазин в данные перед сохранением
        data = request.data.copy()
        data["shop"] = shop.id  # Привязываем бронирование к конкретному магазину
        serializer = BookingSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Токен бота (ОСТОРОЖНО, лучше хранить его в настройках!)
TELEGRAM_BOT_TOKEN = "7222921497:AAHdC-9gxrjaTHlItXjkZafA_7ldGVuPwTE"

def send_message(request, shop_url, employee_id):
    """Форма для ввода сообщения"""
    shop = get_object_or_404(UserSettings, website_url=shop_url)
    employee = get_object_or_404(Employee, id=employee_id)

    if request.method == "POST":
        message_text = request.POST.get("message", "").strip()
        if message_text:
            return redirect('send_message_process', shop_url=shop_url, employee_id=employee.id)

    return render(request, "custom_admin/send_message.html", {
        "employee": employee,
        "shop": shop
    })


def send_message_process(request, shop_url, employee_id):
    """Отправляет сообщение через Telegram бота"""
    shop = get_object_or_404(UserSettings, website_url=shop_url)
    employee = get_object_or_404(Employee, id=employee_id)

    if request.method == "POST":
        message_text = request.POST.get("message", "").strip()

        if not message_text:
            messages.error(request, "Сообщение не может быть пустым!")
            return redirect('send_message', shop_url=shop.website_url, employee_id=employee.id)

        if not employee.user_id_tg:
            messages.error(request, "У сотрудника нет Telegram ID!")
            return redirect('send_message', shop_url=shop.website_url, employee_id=employee.id)

        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"  # ✅ Используем фиксированный токен
        data = {
            "chat_id": employee.user_id_tg,
            "text": message_text,
            "parse_mode": "HTML"
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

    return redirect('send_message', shop_url=shop.website_url, employee_id=employee.id)


@api_view(['GET'])
def task_list_api(request):
    tasks = Task.objects.all()
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)

class TaskCalendarView(View):
    def get(self, request, shop_url):
        shop = get_object_or_404(UserSettings, website_url=shop_url)
        return render(request, "custom_admin/order_calendar.html", {"shop": shop})


def task_events(request, shop_url):
    shop = get_object_or_404(UserSettings, website_url=shop_url)

    # Бронирования
    bookings = Booking.objects.filter(employee__shop=shop)
    booking_events = [
        {
            "title": booking.service_name,
            "start": f"{booking.date}T{booking.start_time}",
            "end": f"{booking.date}T{booking.end_time}",
            "color": "#36A2EB"  # Синий для бронирований
        }
        for booking in bookings
    ]

    # Задачи
    tasks = Task.objects.filter(shop=shop)
    task_events = [
        {
            "title": task.description,
            "start": f"{task.date}T{task.time}",
            "end": f"{task.date}T{task.end_time}" if task.end_time else f"{task.date}T{task.time}",
            "color": "#FF6384"  # Красный для задач
        }
        for task in tasks
    ]

    # Объединяем бронирования и задачи
    events = booking_events + task_events

    return JsonResponse(events, safe=False)




# 📌 Список задач + Фильтрация
def task_list(request, shop_url):
    # Получаем конкретный магазин
    shop = get_object_or_404(UserSettings, website_url=shop_url)

    # Фильтруем задачи только по этому магазину
    tasks = Task.objects.filter(shop=shop)  # Добавь связь Task → UserSettings

    # Фильтрация по дате и номеру комнаты
    date_filter = request.GET.get('date', None)
    room_filter = request.GET.get('room', None)
    if date_filter:
        tasks = tasks.filter(date=date_filter)
    if room_filter:
        tasks = tasks.filter(room=room_filter)

    return render(request, 'custom_admin/apps.html', {'tasks': tasks, 'shop': shop})



def add_task(request, shop_url):  # Получаем `shop_url` из URL
    shop = get_object_or_404(UserSettings, website_url=shop_url)  # Находим магазин

    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.shop = shop  # Привязываем задачу к магазину
            task.save()
            return redirect('task_list', shop_url=shop_url)  # Перенаправляем на список задач

    else:
        form = TaskForm()

    employees = Employee.objects.all()  # Получаем всех сотрудников
    return render(request, 'custom_admin/task_form.html', {'form': form, 'employees': employees, 'shop': shop})

def edit_task(request, shop_url, task_id):
    shop = get_object_or_404(UserSettings, website_url=shop_url)
    task = get_object_or_404(Task, id=task_id, shop=shop)

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list', shop_url=shop_url)  # Редирект с shop_url

    else:
        form = TaskForm(instance=task)

    employees = Employee.objects.all()
    return render(request, 'custom_admin/task_form.html', {
        'form': form,
        'employees': employees,
        'shop': shop,
        'task': task
    })




# 📌 Удаление задачи
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    shop_url = request.GET.get("shop_url")  # Забираем shop_url из URL

    if request.method == "GET":
        task.delete()
        return redirect("task_list", shop_url)  # Передаем shop_url при редиректе

    return render(request, 'custom_admin/task_confirm_delete.html', {'task': task})




@csrf_exempt  # Если используешь CSRF-токен в шаблоне, эту строку можно убрать
def update_booking_status(request, shop_url, booking_id):
    """Обновление статуса бронирования для конкретного магазина"""
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Получаем JSON-данные
            status_id = data.get("status_id")

            # Получаем магазин по `website_url`
            shop = get_object_or_404(UserSettings, website_url=shop_url)

            # Проверяем, что бронирование принадлежит этому магазину
            booking = get_object_or_404(Booking, id=booking_id, employee__shop=shop)

            # Проверяем, что статус существует
            status = get_object_or_404(Status, id=status_id)

            # Обновляем статус бронирования
            booking.status = status
            booking.save()

            return JsonResponse({"success": True, "status": status.name})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    
    return JsonResponse({"success": False, "error": "Метод запроса должен быть POST."})

import requests  # Для запроса услуг через API

def booking_create(request, shop_url):
    """Создание бронирования с привязкой к магазину и уведомлением в Telegram"""

    shop = get_object_or_404(UserSettings, website_url=shop_url)  # Находим магазин
    
    # Получаем список услуг (можно добавить try-except на ошибки)
    try:
        services = requests.get("http://127.0.0.1:8000/api/categories/").json()
    except requests.exceptions.RequestException:
        services = []

    employees = Employee.objects.filter(shop=shop)  # Сотрудники только для этого магазина
    statuses = Status.objects.all()

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.shop = shop  # Привязываем к магазину
            booking.status = Status.objects.get(id=request.POST.get("status"))
            booking.save()
            
            # Отправляем уведомление, если есть сотрудник
            employee_id = request.POST.get("employee")
            if employee_id:
                employee = get_object_or_404(Employee, id=employee_id)
                if employee.user_id_tg:
                    message_text = (
                        f"🔔 <b>Новое бронирование</b>\n"
                        f"🏷 Услуга: {booking.service_name}\n"
                        f"📅 Дата: {booking.date}\n"
                        f"⏰ Время: {booking.start_time} - {booking.end_time or '--:--'}\n"
                        f"🚪 Комната: {booking.room_number}\n"
                        f"👥 Гостей: {booking.guest_count}\n"
                        f"📝 Комментарий: {booking.comment or 'Нет'}"
                    )
                    send_telegram_message(employee.user_id_tg, message_text)
                else:
                    messages.warning(request, "У сотрудника нет Telegram ID, уведомление не отправлено.")

            messages.success(request, "Бронирование успешно создано!")
            return redirect('bookings_list', shop_url=shop_url)  # Перенаправление на бронирования магазина
        else:
            print("Ошибки формы:", form.errors)

    else:
        form = BookingForm()

    return render(request, 'custom_admin/booking_form.html', {
        'form': form,
        'services': services,
        'employees': employees,
        'statuses': statuses,
        'shop': shop
    })


def bookings_list(request, shop_url):
    """Отображение списка бронирований для конкретного магазина."""
    shop = get_object_or_404(UserSettings, website_url=shop_url)

    in_progress_status = Status.objects.get(name="В работе")
    bookings = Booking.objects.filter(status=in_progress_status, shop=shop)  # Фильтруем по магазину

    statuses = Status.objects.all()
    
    return render(request, "custom_admin/bookings.html", {
        "bookings": bookings,
        "statuses": statuses,
        "shop": shop
    })



def archive_list(request, shop_url):
    """Архив бронирований для конкретного магазина"""
    # 1️⃣ Проверяем, что магазин существует
    shop = get_object_or_404(UserSettings, website_url=shop_url)

    # 2️⃣ Фильтруем архивные бронирования по магазину
    archive_statuses = Status.objects.filter(name__in=["Отменен", "Выполнено"])
    archived_bookings = Booking.objects.filter(status__in=archive_statuses, employee__shop=shop)

    # 3️⃣ Передаём статусы (для смены)
    statuses = Status.objects.all()

    return render(request, 'custom_admin/archive.html', {
        'bookings': archived_bookings,
        'statuses': statuses,
        'shop': shop
    })

def employees(request):
    employees = Employee.objects.all()  # Получаем всех сотрудников
    return render(request, "custom_admin/employees.html", {"employees": employees})  





def employees_list(request, shop_url):
    shop = get_object_or_404(UserSettings, website_url=shop_url)  # Фильтруем по магазину
    employees = Employee.objects.filter(shop=shop)  # Только сотрудники конкретного магазина
    
    return render(request, 'custom_admin/employees.html', {'employees': employees, 'shop': shop})


def employee_create(request, shop_url):
    shop = get_object_or_404(UserSettings, website_url=shop_url)

    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            employee = form.save(commit=False)
            employee.shop = shop  # Привязываем сотрудника к магазину
            employee.save()
            return redirect('employees', shop_url=shop_url)
    else:
        form = EmployeeForm()

    return render(request, 'custom_admin/employee_form.html', {'form': form, 'shop': shop})


def employee_edit(request, shop_url, pk):
    shop = get_object_or_404(UserSettings, website_url=shop_url)
    employee = get_object_or_404(Employee, pk=pk, shop=shop)  # Фильтруем по магазину

    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employees_list', shop_url=shop_url)
    else:
        form = EmployeeForm(instance=employee)

    return render(request, 'custom_admin/employee_form.html', {'form': form, 'shop': shop})


def employee_delete(request, shop_url, pk):
    shop = get_object_or_404(UserSettings, website_url=shop_url)
    employee = get_object_or_404(Employee, pk=pk, shop=shop)  # Удаляем только из текущего магазина

    if request.method == 'POST':
        employee.delete()
        return redirect('employees_list', shop_url=shop_url)

    return render(request, 'custom_admin/employee_confirm_delete.html', {'employee': employee, 'shop': shop})

class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        website_url = self.kwargs.get("shop_url")  # Получаем URL из запроса
        shop = get_object_or_404(UserSettings, website_url=website_url)  # Ищем магазин
        return Order.objects.filter(shop=shop).order_by("-created_at")

    def perform_create(self, serializer):
        website_url = self.kwargs.get("shop_url")  # Получаем URL из запроса
        shop = get_object_or_404(UserSettings, website_url=website_url)  # Ищем магазин
        serializer.save(shop=shop)  # Сохраняем заказ с привязкой к магазину





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


def employees(request, shop_url):
    shop = get_object_or_404(UserSettings, website_url=shop_url)  # Получаем магазин по URL
    employees = Employee.objects.filter(shop=shop)  # Получаем только сотрудников этого магазина
    return render(request, "custom_admin/employees.html", {
        "employees": employees,
        "shop": shop
    })



def purchase_stats(request):
    return render(request, "custom_admin/purchase_stats.html")


def orders(request, shop_url):
    shop = get_object_or_404(UserSettings, website_url=shop_url)  # Используем правильное поле
    orders = Order.objects.filter(shop=shop).order_by("-status", "-created_at")  
    employees = Employee.objects.filter(shop=shop)
    new_orders_count = orders.filter(status="new").count()  

    return render(request, "custom_admin/orders.html", {
        "orders": orders,
        "employees": employees,
        "new_orders_count": new_orders_count,
        "shop": shop
    })
