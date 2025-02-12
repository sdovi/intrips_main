from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ChatMessage
from .serializers import ChatMessageSerializer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from django.db.models import Q
from django.db.models import Exists, OuterRef




from django.http import JsonResponse
from .models import ChatMessage
from django.db.models import Exists, OuterRef

def unread_messages_count(request):
    """Возвращает количество непрочитанных сообщений"""
    unread_count = ChatMessage.objects.filter(
        is_admin=False
    ).annotate(
        has_reply=Exists(ChatMessage.objects.filter(replied_to=OuterRef('id')))
    ).filter(has_reply=False).count()
    
    return JsonResponse({"unread_count": unread_count})



class ChatAPIView(APIView):
    def get(self, request):
        """
        Получение сообщений или количества непрочитанных.
        """
        user_id = request.query_params.get('user_id')
        show_unanswered = request.query_params.get('unanswered', False)
        get_unread_count = request.query_params.get('unread_count', False)

        if get_unread_count and get_unread_count.lower() == 'true':
            unread_count = ChatMessage.objects.filter(
                is_admin=False
            ).annotate(
                has_reply=Exists(
                    ChatMessage.objects.filter(replied_to=OuterRef('id'))
                )
            ).filter(has_reply=False).count()
            return Response({"unread_count": unread_count})

        if show_unanswered and show_unanswered.lower() == 'true':
            messages = ChatMessage.objects.filter(
                is_admin=False
            ).annotate(
                has_reply=Exists(
                    ChatMessage.objects.filter(replied_to=OuterRef('id'))
                )
            ).filter(has_reply=False).order_by('timestamp')
        else:
            messages = ChatMessage.objects.filter(user_id=user_id).order_by('timestamp')

        serializer = ChatMessageSerializer(messages, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Отправка нового сообщения.
        Если админ отвечает, то отмечаем, что он ответил.
        """
        data = request.data
        replied_to_id = data.get('replied_to')

        serializer = ChatMessageSerializer(data=data)
        if serializer.is_valid():
            message = serializer.save()

            # Если это ответ админа, привязываем его к сообщению пользователя
            if message.is_admin and replied_to_id:
                replied_message = ChatMessage.objects.filter(id=replied_to_id, is_admin=False).first()
                if replied_message:
                    message.replied_to = replied_message
                    message.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
