from collections import OrderedDict
from django.conf import settings
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomListViewPageNumberPagination(PageNumberPagination):

    def get_page_size(self, request):
        page_size = request.query_params.get("pageSize", self.page_size)
        max_page_size = settings.MAX_PAGE_SIZE
        return min(int(page_size), max_page_size)

    def get_paginated_response (self, data):
        return Response(
            OrderedDict([
                ("count", self.page.paginator.count),
                ("next", self.get_next_link()),
                ("previous", self.get_previous_link()),
                ("page", self.page.number),
                ("pageSize", self.get_page_size(self.request)),
                ("results", data),
            ])
        )
