from core import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'news', views.NewsViewSet, basename='news')
router.register(r'categories', views.CategoryViewSet, basename='categories')

urlpatterns = router.urls