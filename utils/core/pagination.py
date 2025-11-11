from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict

from utils.core.response_wrappers import OKResponse


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data):
        return OKResponse(
            data=OrderedDict(
                [
                    ("count", self.page.paginator.count),  # total objects available
                    ("results_count", len(data)),  # total objects returned
                    ("next", self.get_next_link()),
                    ("previous", self.get_previous_link()),
                    ("total_pages", self.page.paginator.num_pages),
                    ("current_page", self.page.number),
                    (
                        "next_page",
                        self.page.next_page_number() if self.page.has_next() else None,
                    ),
                    (
                        "previous_page",
                        (
                            self.page.previous_page_number()
                            if self.page.has_previous()
                            else None
                        ),
                    ),
                    ("page_size", self.page.paginator.per_page),
                    ("results", data),
                ]
            )
        )
