from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, MenuItemViewSet,HeadertextViewSet,SubCategoryViewSet

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='category')
router.register('menu-items', MenuItemViewSet, basename='menu-item')
router.register('header-text', HeadertextViewSet, basename='header-text')
router.register('subcategories', SubCategoryViewSet, basename='subcategory')


urlpatterns = router.urls
