#!/usr/bin/env python3
"""A script for FIFO caching system
"""
BaseCaching = __import__('base_caching').BaseCaching
from collections import deque


class LIFOCache (BaseCaching):
    """BasicCache inherits from BaseCaching and is a caching system"""
    def __init__(self):
        """Initialize BasicCache"""
        super().__init__()
        self.cache = []


    def put(self, key, item):
        """Add an item in the cache"""
        if key is None or item is None:
            return

        self.cache_data[key] = item
        self.cache.append(key)
        if len(self.cache) > BaseCaching.MAX_ITEMS:
            discarded_key = self.cache.pop(0)
            del self.cache_data[discarded_key]
            print("DISCARD:", discarded_key)


    def get(self, key):
        """Get an item by key"""
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data[key]
