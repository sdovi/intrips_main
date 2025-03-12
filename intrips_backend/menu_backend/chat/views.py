from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ChatMessage
from .serializers import ChatMessageSerializer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from django.db.models import Q
from django.db.models import Exists, OuterRef

from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Exists, OuterRef
from .models import ChatMessage
from .serializers import ChatMessageSerializer
from main.models import UserSettings
from django.contrib.auth.decorators import login_required


from django.http import JsonResponse
from .models import ChatMessage
from django.db.models import Exists, OuterRef
from django.shortcuts import redirect
from django.utils.timezone import now

from django.db import models  # Добавляем models для работы с DateTimeField
from django.db.models import Max  # Импортируем Max


def chat_admin_view(request, shop_url, user_id=None):
    # Получаем магазин по URL
    shop = get_object_or_404(UserSettings, website_url=shop_url)

    # Группируем сообщения по user_id (только от клиентов)
    users = (
        ChatMessage.objects.filter(shop=shop, is_admin=False)
        .values("user_id")
        .annotate(last_time=Max("timestamp", output_field=models.DateTimeField()))
        .order_by("-last_time")
    )

    # Если выбран конкретный пользователь – загружаем его переписку
    messages = ChatMessage.objects.filter(shop=shop, user_id=user_id).order_by("timestamp") if user_id else []

    # Если пришёл POST-запрос (админ отвечает)
    if request.method == "POST" and user_id:
        message_text = request.POST.get("message")
        if message_text:
            ChatMessage.objects.create(
                shop=shop,
                user_id=user_id,
                message=message_text,
                is_admin=True,
                timestamp=now()
            )
        return redirect("chat_admin_user", shop_url=shop_url, user_id=user_id)

    context = {
        "shop": shop,
        "users": users,
        "messages": messages,
        "selected_user": user_id,
    }
    return render(request, "chat_admin.html", context)


class ChatAPIView(APIView):
    """API для работы с сообщениями чата в конкретном магазине"""

    def get(self, request, shop_url):
        shop = get_object_or_404(UserSettings, website_url=shop_url)
        user_id = request.query_params.get("user_id")  # Фильтрация по user_id

        show_unanswered = request.query_params.get("unanswered", "false").lower() == "true"
        get_unread_count = request.query_params.get("unread_count", "false").lower() == "true"

        if get_unread_count:
            unread_count = ChatMessage.objects.filter(shop=shop, user_id=user_id, is_admin=False) \
                .annotate(has_reply=Exists(ChatMessage.objects.filter(replied_to=OuterRef("id")))) \
                .filter(has_reply=False).count()
            return Response({"unread_count": unread_count})

        messages = ChatMessage.objects.filter(shop=shop)

        # Добавляем разделение чатов
        if user_id:
            messages = messages.filter(user_id=user_id)

        messages = messages.order_by("timestamp")

        if show_unanswered:
            messages = messages.filter(is_admin=False) \
                .annotate(has_reply=Exists(ChatMessage.objects.filter(replied_to=OuterRef("id")))) \
                .filter(has_reply=False)

        serializer = ChatMessageSerializer(messages, many=True)
        return Response(serializer.data)

    def post(self, request, shop_url):
        """Добавление нового сообщения или ответа"""
        shop = get_object_or_404(UserSettings, website_url=shop_url)
        data = request.data

        if "user_id" not in data:
            return Response({"error": "user_id обязателен"}, status=status.HTTP_400_BAD_REQUEST)

        data["shop"] = shop.id

        serializer = ChatMessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@login_required
def unread_messages_count(request, shop_url):
    """Возвращает количество только неотвеченных сообщений"""
    try:
        shop = get_object_or_404(UserSettings, website_url=shop_url)

        unread_count = ChatMessage.objects.filter(
            shop=shop,
            is_admin=False,  # Только сообщения от клиентов
        ).annotate(
            has_reply=Exists(ChatMessage.objects.filter(replied_to=OuterRef("id")))  # Проверяем есть ли ответ
        ).filter(
            has_reply=False  # Берем только те, у которых нет ответа
        ).count()

        return JsonResponse({"unread_count": unread_count})

    except UserSettings.DoesNotExist:
        return JsonResponse({"error": "Магазин не найден"}, status=404)
