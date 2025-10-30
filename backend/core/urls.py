from core import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'news', views.NewsViewSet, basename='news')
router.register(r'preferences', views.CategoryViewSet, basename='preferences')
router.register(r'users/me/preferences', views.UserPreferenceViewSet, basename='user-preferences')

urlpatterns = router.urls