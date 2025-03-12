from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings  # Импортируем settings
from django.conf.urls.static import static  # Импортируем static
from .views import (
    CategoryViewSet, MenuItemViewSet, HeadertextViewSet, SubCategoryViewSet,
    get_all_data, UserSettingsViewSet
)

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='category')
router.register('menu-items', MenuItemViewSet, basename='menu-item')
router.register('header-text', HeadertextViewSet, basename='header-text')
router.register('subcategories', SubCategoryViewSet, basename='subcategory')

router.register('info_magaz', UserSettingsViewSet, basename='user-settings')

urlpatterns = [
    path("all-data/", get_all_data, name="get_all_data"),  # 👈 Добавили новый GET-запрос
    path("", include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # 👈 Добавляем обработку медиафайлов