from core import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'news', views.NewsViewSet, basename='news')
router.register(r'preferences', views.CategoryViewSet, basename='preferences')

urlpatterns = router.urls