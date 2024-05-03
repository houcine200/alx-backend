#!/usr/bin/env python3
"""Hypermedia pagination generating script"""
import csv
import math
from typing import List


def index_range(page, page_size):
    """Return a tuple of size two
    containing a start index and an end index
    """
    start_index = (page - 1) * page_size
    end_index = page * page_size
    page_data = (start_index, end_index)
    return page_data


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """Get page from the dataset"""
        assert isinstance(page, int) and page > 0
        assert isinstance(page_size, int) and page_size > 0

        dataset = self.dataset()

        start_index, end_index = index_range(page, page_size)

        if start_index >= len(dataset):
            return []

        page_data = dataset[start_index:end_index]

        return page_data

    def get_hyper(self, page: int = 1, page_size: int = 10) -> dict:
        """returns a dictionary of hypermedia keys and values
        """
        page_data = self.get_page(page, page_size)

        page_size = len(page_data)
        total_items = len(self.dataset())
        total_pages = total_items // page_size if page_size > 0 else 0
        next_page = page + 1 if page < total_pages else None
        prev_page = page - 1 if page > 1 else None

        hyper_info_dict = {
            "page_size": len(page_data),
            "page": page,
            "data": page_data,
            "next_page": next_page,
            "prev_page": prev_page,
            "total_pages": total_pages
        }

        return hyper_info_dict
