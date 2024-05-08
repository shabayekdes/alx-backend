#!/usr/bin/env python3
"""Task 1: Simple helper function
"""
from typing import Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """Retrieves the index range from a given page and page size.
    """

    return ((page - 1) * page_size, page * page_size)
