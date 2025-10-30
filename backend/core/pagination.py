from rest_framework.pagination import PageNumberPagination


# Create your views here.
class NewsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10
