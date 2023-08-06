
from functools import partial
from itertools import islice


def take(n, iterable):
    return list(islice(iterable, n))


def chunk(iterable, n):
    return iter(partial(take, n, iter(iterable)), [])
