#!/usr/bin/env python3
"""A script for FIFO caching system
"""
BaseCaching = __import__('base_caching').BaseCaching


class LIFOCache (BaseCaching):
    """BasicCache inherits from BaseCaching and is a caching system"""
    def __init__(self):
        """Initialize BasicCache"""
        super().__init__()

    def put(self, key, item):
        """Add an item in the cache"""
        if key is None or item is None:
            return

        if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            last_key = next(reversed(self.cache_data))
            print(f'DISCARD: {last_key}')
            del self.cache_data[last_key]
        self.cache_data[key] = item

    def get(self, key):
        """Get an item by key"""
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data[key]
