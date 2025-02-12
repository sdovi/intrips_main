from rest_framework.viewsets import ModelViewSet
from .models import Category, MenuItem,Headertext,SubCategory
from .serializers import CategorySerializer, MenuItemSerializer,HeadertextSerializer, SubCategorySerializer



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
