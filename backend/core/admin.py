from django.contrib import admin
from core.models import News, Category, UserPreference
# Register your models here.

admin.site.register(Category)
admin.site.register(News)
admin.site.register(UserPreference)