from core.models import News, Category, UserPreference
from core.serializers import NewsSerializer, NewsCreateSerializer, CategorySerializer, UserPreferenceSerializer
from core.pagination import NewsPagination
from datetime import timedelta
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    pagination_class = NewsPagination
    permission_classes = [ IsAuthenticated ]

    # Filter by period
    def get_queryset(self):
        queryset = super().get_queryset()
        period = self.request.query_params.get('period')
        now = timezone.now()

        if period == 'day':
            queryset = queryset.filter(created_at__gte=now - timedelta(days=1))
        elif period == 'week':
            queryset = queryset.filter(created_at__gte=now - timedelta(weeks=1))
        elif period == 'month':
            queryset = queryset.filter(created_at__gte=now - timedelta(days=30))

        return queryset.order_by('-created_at')
        
    def retrieve(self, request, pk=None):
        news = get_object_or_404(self.queryset, pk=pk)
        serializer = NewsSerializer(news)
        return Response(serializer.data)

    def create(self, request):
        serializer = NewsCreateSerializer(data=request.data)
        if serializer.is_valid():
            if "category_id" in serializer.data:
                category_id = serializer.data.get('category_id')
                try:
                    category = Category.objects.get(id=category_id)
                except Category.DoesNotExist:
                    return Response({"error": "Category not found!"}, status=status.HTTP_404_NOT_FOUND)

                news = News.objects.create(
                    title=serializer.data['title'],
                    content=serializer.data['content'],
                    category_id=category.id
                )
                serializer = NewsSerializer(news)
                return Response({
                    "message": "News Created Sucessfully!", 
                    "data": serializer.data
                }, status=status.HTTP_201_CREATED
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        try:
            news = News.objects.get(pk=pk)
        except News.DoesNotExist:
            return Response({"error": "News not found!"}, status=status.HTTP_404_NOT_FOUND)

        serializer = NewsSerializer(news, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "News updated sucessfully", 
                "data": serializer.data
                }, status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            news = News.objects.get(pk=pk)
        except News.DoesNotExist:
            return Response({"error": "News not found!"}, status=status.HTTP_404_NOT_FOUND)

        news.delete()
        return Response({"message": "News deleted sucessfully!"}, status=status.HTTP_204_NO_CONTENT)

class CategoryViewSet(viewsets.ViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [ IsAuthenticated ]

    def list(self, request):
        if request.method == "GET":
            serializer = CategorySerializer(self.queryset, many=True)
            return Response(serializer.data)
        
    def retrieve(self, request, pk=None):
        category = get_object_or_404(self.queryset, pk=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def create(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Category created sucessfully", 
                "data": serializer.data
                }, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({"error": "Category not found!"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CategorySerializer(category, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Category updated sucessfully", 
                "data": serializer.data
                }, status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({"error": "Category not found!"}, status=status.HTTP_404_NOT_FOUND)

        category.delete()
        return Response({"message": "Category deleted sucessfully!"}, status=status.HTTP_204_NO_CONTENT)

class UserPreferenceViewSet(viewsets.ViewSet):
    queryset = UserPreference.objects.all()
    serializer_class = UserPreferenceSerializer
    permission_classes = [ IsAuthenticated ]

    def get_profile(self, request):
        user_preference, _ = UserPreference.objects.get_or_create(user=request.user)
        return user_preference

    def list(self, request):
        user = self.get_profile(request)
        serializer = UserPreferenceSerializer(user)
        return Response(serializer.data)

    def update(self, request, pk=None):
        user = self.get_profile(request)
        serializer = UserPreferenceSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)