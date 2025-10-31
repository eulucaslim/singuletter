from django.urls import path, include
from core import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(
    r'news', 
    views.NewsViewSet, 
    basename='news'
)
router.register(
    r'preferences', 
    views.CategoryViewSet, 
    basename='preferences'
)
user_preferences = views.UserPreferenceViewSet.as_view({
    'get': 'list',
    'put': 'update'
})

urlpatterns = [
    path('', include(router.urls)),
    path('users/me/preferences/', user_preferences, name='user-preferences'),
]
