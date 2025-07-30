from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class PageNotFoundException(NotFound):
    status_code = status.HTTP_200_OK


class CustomPagination(PageNumberPagination):
    """
    A Custom Pagination class.
    """

    page_size_query_param = "page_size"
    page_query_param = "page"
    total_count = 0

    def get_paginated_response(self, data):
        return Response(
            {
                "count": self.page.paginator.count,
                "page_count": self.page.paginator.num_pages,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "results": data,
            }
        )

    def paginate_queryset(self, queryset, request, view=None):
        page = request.query_params.get(self.page_query_param, None)
        page_size = request.query_params.get(self.page_size_query_param, None)

        if page is None and page_size is None:
            return None

        return super().paginate_queryset(queryset, request, view)

    def get_unpaginated_response(self, serialized_data):
        paginated_data = {
            "count": len(serialized_data),
            "page_count": "",
            "next": "",
            "previous": "",
            "results": serialized_data,
        }
        return paginated_data
