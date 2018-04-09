from typing import List


def has_duplicates(values: List):
    unique_values = set(values)
    return len(unique_values) != len(values)
