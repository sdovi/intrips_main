from rest_framework import serializers
from .models import Category, MenuItem, Headertext, SubCategory

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'


class HeadertextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Headertext
        fields = '__all__'



class CategorySerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = '__all__'

    def get_photo_url(self, obj):
        if obj.photo:
            return self.context['request'].build_absolute_uri(obj.photo.url)
        return None



class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'
