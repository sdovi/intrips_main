from django.urls import path
from .views import ChatAPIView, unread_messages_count
from django.shortcuts import render
from custom_admin.models import Order

def chat_page(request):
    new_orders_count = Order.objects.filter(status="new").count()
    return render(request, 'chat.html', {"new_orders_count": new_orders_count})

urlpatterns = [
    
    path('unread_count/', unread_messages_count, name='unread_count'),
    path('messages/', ChatAPIView.as_view(), name='chat_api'),
    path('chat/', chat_page, name='chat_page'),
]
