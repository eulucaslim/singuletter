from core.models import News
from rest_framework import serializers

class NewsSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = News
        fields = ('id', 'title', 'content', 'category')