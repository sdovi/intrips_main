from django.urls import path
from . import views
from .views import OrderListCreateView
from .views import employee_create, employee_edit, employee_delete, booking_create, bookings_list, employees, employees_list, update_booking_status, task_list, add_task, edit_task, delete_task, TaskCalendarView, task_events, task_list_api, send_message, send_message_process, bookings, confirm_order, money_stats_view,EmployeeListView

from .views import agreement_categories, info_cards, info_card_detail, agreement_category_detail
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('api/agreement_categories/', agreement_categories, name='agreement_categories'),
    path('api/agreement_categories/<int:category_id>/', agreement_category_detail, name='agreement_category_detail'),
    path('api/info_cards/', info_cards, name='info_cards'),
    path('api/info_cards/<int:card_id>/', info_card_detail, name='info_card_detail'),
    path('employee/api/', EmployeeListView.as_view(), name='employee_api'),
    
    path('money-stats/', money_stats_view, name='money_stats'),
    
    
    # path("product-stats/", views.product_stats_view, name="product_stats"),
    
    
    path('confirm_order/<int:order_id>/', confirm_order, name='confirm_order'),
    
    
    
    
    
    
    path("users/", views.user_list, name="user_list"),
    path("delete_user/<int:user_id>/", views.delete_user, name="delete_user"),
    path("login/", auth_views.LoginView.as_view(template_name="custom_admin/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),
    path("register/", views.register_admin, name="register_admin"),
    
    path('api/bookings/', bookings, name='bookings'),  # тут твой путь

    path('send_message/<int:employee_id>/', send_message, name='send_message'),
    path('send_message_process/<int:employee_id>/', send_message_process, name='send_message_process'),
    
    
    path("", views.dashboard, name="dashboard"), 
    path("chat/", views.chat_guest, name="chat_guest"),
    path("apps/", views.apps, name="apps"),
    path("services/", views.services, name="services"),
    path("calendar/", views.order_calendar, name="order_calendar"),
    # path("stats/", views.purchase_stats, name="purchase_stats"),
    path('stats/', views.purchase_stats_view, name='purchase_stats'),
    path("archive/", views.archive_list, name="archive_list"),
    path("orders/", OrderListCreateView.as_view(), name="orders_views"),
    path("orders_view/", views.orders, name="orders"),
    
    
    
    
    path("employees/", employees, name="employees"),
    path('employees1/', employees_list, name='employees_list'),
    path('employees/new/', employee_create, name='employee_create'),
    path('employees/edit/<int:pk>/', employee_edit, name='employee_edit'),
    path('employees/delete/<int:pk>/', employee_delete, name='employee_delete'),
    
    path('bookings/new/', booking_create, name='booking_create'),
    path('bookings/', bookings_list, name='bookings_list'),
    
    path('update_booking_status/<int:booking_id>/', update_booking_status, name='update_booking_status'),

    
    
    
    path('api/tasks/', task_list_api, name='task_list_api'),
    path('get/', task_list, name='task_list'),
    path('add/', add_task, name='add_task'),
    path('edit/<int:task_id>/', edit_task, name='edit_task'),
    path('delete/<int:task_id>/', delete_task, name='delete_task'),
    



    path('calendar/', TaskCalendarView.as_view(), name='task_calendar'),
    path("calendar/events/", task_events, name="task_events"),





] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
