from rest_framework.viewsets import ModelViewSet
from .models import Category, MenuItem,Headertext,SubCategory
from .serializers import CategorySerializer, MenuItemSerializer,HeadertextSerializer, SubCategorySerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import UserSettings, SubCategory, Category, MenuItem, Headertext
from .serializers import (
    UserSettingsSerializer, SubCategorySerializer, CategorySerializer, MenuItemSerializer, HeadertextSerializer
)
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import UserSettings, SubCategory, Category, MenuItem, Headertext
from .serializers import UserSettingsSerializer, SubCategorySerializer, CategorySerializer, MenuItemSerializer, HeadertextSerializer, UserVitrinaSerializer


class UserSettingsViewSet(viewsets.ModelViewSet):
    queryset = UserSettings.objects.all()
    serializer_class = UserVitrinaSerializer

@api_view(["GET"])
def get_all_data(request):
    user_settings_list = UserSettings.objects.all()

    response_data = []

    for user_settings in user_settings_list:
        response_data.append({
            "user_settings": UserSettingsSerializer(user_settings).data,
            "subcategories": SubCategorySerializer(
                SubCategory.objects.filter(user_settings=user_settings), many=True
            ).data,
            "categories": CategorySerializer(
                Category.objects.filter(user_settings=user_settings), many=True
            ).data,
            "menu_items": MenuItemSerializer(
                MenuItem.objects.filter(user_settings=user_settings), many=True
            ).data,
            "header_texts": HeadertextSerializer(
                Headertext.objects.filter(user_settings=user_settings), many=True
            ).data,
        })

    return Response(response_data)




class SubCategoryViewSet(ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class MenuItemViewSet(ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

class HeadertextViewSet(ModelViewSet):
    queryset = Headertext.objects.all()
    serializer_class = HeadertextSerializer
