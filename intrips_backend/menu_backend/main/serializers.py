from rest_framework import serializers
from .models import UserSettings, SubCategory, Category, MenuItem, Headertext

class UserVitrinaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSettings
        fields = '__all__'
        
        
        
        

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    sub_category = SubCategorySerializer()  # Вложенный сериализатор

    class Meta:
        model = Category
        fields = '__all__'


class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer()  # Вложенный сериализатор

    class Meta:
        model = MenuItem
        fields = '__all__'


class HeadertextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Headertext
        fields = '__all__'


class UserSettingsSerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True, read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    menu_items = MenuItemSerializer(many=True, read_only=True)
    header_texts = HeadertextSerializer(many=True, read_only=True)

    class Meta:
        model = UserSettings
        fields = '__all__'
