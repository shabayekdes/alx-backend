#!/usr/bin/env python3
"""Task 5: Least Frequently Used caching module.
"""
from collections import defaultdict
from base_caching import BaseCaching

class LFUCache(BaseCaching):
    """Least Frequently Used (LFU) caching implementation.

    Inherits from BaseCaching and provides a caching system based on the LFU eviction policy.

    Attributes:
        cache_data (dict): Dictionary to store key-value pairs of cached items.
        freq_map (defaultdict): Dictionary to map item frequencies to lists of keys with that frequency.
        key_freq (dict): Dictionary to track the current frequency of each cached key.
        min_freq (int): Minimum frequency among all cached items.
    """

    def __init__(self):
        """Initializes the LFU cache.

        Overrides the BaseCaching class constructor to set up LFU-specific attributes.
        """
        super().__init__()
        self.freq_map = defaultdict(list)
        self.key_freq = {}
        self.min_freq = 0

    def _update_frequency(self, key):
        """Updates the frequency of a cached key.

        Args:
            key: The key whose frequency needs to be updated.
        """
        freq = self.key_freq.get(key, 0)
        new_freq = freq + 1
        self.key_freq[key] = new_freq
        self.freq_map[new_freq].append(key)
        if freq > 0:
            self.freq_map[freq].remove(key)
            if not self.freq_map[freq]:  # If no keys left at this frequency
                if freq == self.min_freq:
                    self.min_freq += 1

    def put(self, key, item):
        """Adds or updates an item in the LFU cache.

        If the cache size exceeds the maximum allowed items, it evicts the least frequently used item(s).

        Args:
            key: The key of the item to be added or updated.
            item: The value of the item to be added or updated.

        If key or item is None, this method does nothing.
        """
        if key is None or item is None:
            return
        if key in self.cache_data:
            self.cache_data[key] = item
            self._update_frequency(key)
        else:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                # Evict least frequency used item
                while self.min_freq not in self.freq_map or not self.freq_map[self.min_freq]:
                    self.min_freq += 1
                lfu_key = self.freq_map[self.min_freq][0]
                del self.cache_data[lfu_key]
                self.freq_map[self.min_freq].pop(0)
                if not self.freq_map[self.min_freq]:  # If no keys left at this frequency
                    self.min_freq += 1
                print(f"DISCARD: {lfu_key}")
            self.cache_data[key] = item
            self._update_frequency(key)

    def get(self, key):
        """Retrieves an item from the LFU cache.

        If the requested key exists in the cache, its frequency is updated.

        Args:
            key: The key of the item to be retrieved.

        Returns:
            The value associated with the specified key, or None if the key is not found.
        """
        if key is None or key not in self.cache_data:
            return None
        self._update_frequency(key)
        return self.cache_data[key]

    def print_cache(self):
        """Prints the current state of the LFU cache.

        Displays the key-value pairs stored in the cache.
        """
        print("Current cache:")
        for key in self.cache_data:
            print(f"{key}: {self.cache_data[key]}")
