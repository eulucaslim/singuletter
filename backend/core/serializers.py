from core.models import News, Category, UserPreference
from rest_framework import serializers

class NewsSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(required=False)
    category_name = serializers.CharField(source='category.name', read_only=True)
    class Meta:
        model = News
        fields = ('id', 'title', 'content', 'category_id', 'category_name')

class NewsCreateSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(required=False)
    category_name = serializers.CharField()
    class Meta:
        model = News
        fields = ('title', 'content', 'category_id', 'category_name')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ["created_at"]

class UserPreferenceSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True, required=False)
    category_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        write_only=True,
        source="categories",
        queryset=Category.objects.all(),
        required=False
    )
    class Meta:
        model = UserPreference
        fields = ["categories", "category_ids"]