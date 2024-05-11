#!/usr/bin/env python3
"""Task 1: FIFO caching
"""
from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """A class FIFOCache that inherits from BaseCaching
    """

    def __init__(self):
        """_summary_
        """
        super().__init__()

    def put(self, key, item):
        """assign to the dictionary cache_data
        """
        if key is None or item is None:
            pass
        else:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS \
                    and key not in self.cache_data.keys():
                first_key = next(iter(self.cache_data.keys()))
                del self.cache_data[first_key]
                print("DISCARD: {}". format(first_key))

            self.cache_data[key] = item

    def get(self, key):
        """return the value in cache_data
        """
        if key is None or key not in self.cache_data.keys():
            return None
        return self.cache_data.get(key)
