from core import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'news', views.NewsViewSet, basename='news')

urlpatterns = router.urls