
from functools import partial
from itertools import islice, accumulate
from math import ceil


def take(n, iterable):
    return list(islice(iterable, n))


def chunk(iterable, n):
    return iter(partial(take, n, iter(iterable)), [])


def split_list(arr, ratios):
    """Split array according to ratios. Sum of ratios should be <= 1"""
    to_return = []
    offsets = [0] + list(map(lambda x: ceil(x * len(arr)), accumulate(ratios)))
    for offset_from, offset_to in zip(offsets[:-1], offsets[1:]):
        to_return.append(arr[offset_from:offset_to])
    return to_return
