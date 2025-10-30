from core.models import News, Category
from rest_framework import serializers

class NewsSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = News
        fields = ('id', 'title', 'content', 'category')

class NewsCreateSerializer(serializers.ModelSerializer):
    category = serializers.IntegerField()
    class Meta:
        model = News
        fields = ('title', 'content', 'category')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ["created_at"]