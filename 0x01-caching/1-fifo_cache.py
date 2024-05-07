#!/usr/bin/env python3
"""A script for FIFO caching system
"""
BaseCaching = __import__('base_caching').BaseCaching


class FIFOCache (BaseCaching):
    def __init__(self):
        """Initialize BasicCache"""
        super().__init__()

    def put(self, key, item):
        """Add an item in the cache"""
        if key is None or item is None:
            return
        self.cache_data[key] = item
        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            discarded_key = next(iter(self.cache_data))
            print(f'DISCARD: {discarded_key}')
            del self.cache_data[discarded_key]

    def get(self, key):
        """Get an item by key"""
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data[key]
