from rest_framework.pagination import PageNumberPagination

class CustomPageNumberPagination(PageNumberPagination):
    # default
    page_size = 10
    page_size_query_param = 'page_size'
    # limits abuse
    max_page_size = 100 