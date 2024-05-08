#!/usr/bin/env python3
"""Task 3: Deletion-resilient hypermedia pagination
"""

import csv
import math
from typing import Dict, List, Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """Retrieves the index range from a given page and page size.
    """

    return ((page - 1) * page_size, page * page_size)


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

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

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0
        """
        if self.__indexed_dataset is None:
            dataset = self._load_dataset()
            truncated_dataset = dataset[:1000]
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None,
                        page_size: int = 10) -> Dict:
        """ return all data"""

        if index is None:
            index = 0

        # validate the index
        assert isinstance(index, int)
        assert 0 <= index < len(self.indexed_dataset())
        assert isinstance(page_size, int) and page_size > 0

        data = []  # collect all indexed data
        next_index = index + page_size

        for value in range(index, next_index):
            if self.indexed_dataset().get(value):
                data.append(self.indexed_dataset()[value])
            else:
                value += 1
                next_index += 1

        return {
            'index': index,
            'data': data,
            'page_size': page_size,
            'next_index': next_index
        }
