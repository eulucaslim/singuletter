from core.models import News, Category, UserPreference
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

class UserPreferenceSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
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

    def update(self, instance, validated_data):
        categories = validated_data.get("categories", [])
        instance.categories.set(categories)
        instance.save()
        return instance