#!/usr/bin/env python3
"""A script for LRU caching system"""
from collections import OrderedDict
BaseCaching = __import__('base_caching').BaseCaching


class LRUCache(BaseCaching):
    """LRUCache inherits from BaseCaching and implements LRU caching system"""

    def __init__(self):
        """Initialize LRUCache"""
        super().__init__()
        self.cache_data = OrderedDict()

    def put(self, key, item):
        """Add an item in the cache"""
        if key is None or item is None:
            return


        if key in self.cache_data:
            del self.cache_data[key]
        elif len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            lru_key, _ = self.cache_data.popitem(last=False)
            print("DISCARD:", lru_key)

        self.cache_data[key] = item

    def get(self, key):
        """Get an item by key"""
        if key is None or key not in self.cache_data:
            return None
        
        value = self.cache_data.pop(key)
        self.cache_data[key] = value
        
        return value
