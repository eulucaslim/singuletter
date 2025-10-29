from core.models import News, Category, UserPreference
from core.serializers import NewsSerializer
from rest_framework import viewsets
from rest_framework.response import Response

# Create your views here.

class NewsViewSet(viewsets.ViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

    def list(self, request):
        if request.method == "GET":
            serializer = NewsSerializer(self.queryset, many=True)
            return Response(serializer.data)