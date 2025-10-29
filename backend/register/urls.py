from django.urls import path
from .views import RegisterView

urlpatterns = [
    path('users/', RegisterView.as_view(), name='users'),
]