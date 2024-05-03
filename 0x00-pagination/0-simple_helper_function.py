#!/usr/bin/env python3
""" A script to generate a list for
particular pagination parameters"""


def index_range(page, page_size):
    """Return a tuple of size two
    containing a start index and an end index
    """
    start_index = (page - 1) * page_size
    end_index = page * page_size
    page_data = (start_index, end_index)
    return page_data
