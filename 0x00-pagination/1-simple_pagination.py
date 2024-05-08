#!/usr/bin/env python3
"""Task 1: Simple pagination.
"""
import csv
import math
from typing import List, Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """Retrieves the index range from a given page and page size."""
    return ((page - 1) * page_size, page * page_size)


class Server:
    """Server class to paginate a database of popular baby names."""

    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def _load_dataset(self) -> List[List]:
        """Load dataset from CSV file."""
        if self.__dataset is None:
            try:
                with open(self.DATA_FILE) as f:
                    reader = csv.reader(f)
                    self.__dataset = [row for row in reader][1:]  # Skip header
            except FileNotFoundError:
                print(f"Error: File '{self.DATA_FILE}' not found.")
                self.__dataset = []

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """Retrieves a page of data."""
        assert isinstance(page, int) and isinstance(page_size, int)
        assert page > 0 and page_size > 0

        data = self._load_dataset()
        total_records = len(data)
        total_pages = math.ceil(total_records / page_size)

        if page > total_pages:
            return []

        start, end = index_range(page, page_size)
        return data[start:end]

    def total_pages(self, page_size: int = 10) -> int:
        """Calculates the total number of pages."""
        data = self._load_dataset()
        total_records = len(data)
        return math.ceil(total_records / page_size)
