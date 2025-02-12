from django.urls import path
from .views import ChatAPIView

urlpatterns = [
    path('messages/', ChatAPIView.as_view(), name='chat_api'),
]
