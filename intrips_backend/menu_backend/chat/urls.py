from django.urls import path
from .views import ChatAPIView, unread_messages_count, chat_admin_view
from django.shortcuts import render
from custom_admin.models import Order
from django.shortcuts import render, get_object_or_404, redirect

from main.models import UserSettings  # Импортируем нашу модель магазина
from django.contrib.auth.decorators import login_required, user_passes_test


@login_required(login_url="login")
def chat_page(request, shop_url):
    """Страница чата для конкретного магазина"""
    shop = get_object_or_404(UserSettings, website_url=shop_url)
    return render(request, 'chat.html', {"shop": shop})


urlpatterns = [
    
    path('messages/', ChatAPIView.as_view(), name='chat_api'),
    path('chat/', chat_page, name='chat_page'),
    
    path('<str:shop_url>/unread_count/', unread_messages_count, name='unread_count'),
    path('<str:shop_url>/messages/', ChatAPIView.as_view(), name='chat_api'),
    path('<str:shop_url>/chat/', chat_page, name='chat_page'),
    
    path("<str:shop_url>/admin_chat/", chat_admin_view, name="chat_admin"),
    path("<str:shop_url>/admin_chat/<str:user_id>/", chat_admin_view, name="chat_admin_user"),

]
