from functools import lru_cache

from memory_profiler import profile

import pandas as pd
import numpy as np

@profile
def simple_function():
    a = [1] * (10 ** 6)
    b = [2] * (2 * 10 ** 7)
    del b
    return a

@profile
def simple_function2():
    a = [1] * (10 ** 6)
    b = [2] * (2 * 10 ** 8)
    del b
    return a

@lru_cache
def caching_function(size):
    return np.ones(size)


@profile
def test_caching_function():
    for i in range(10_000):
        caching_function(i)

    for i in range(10_000,0,-1):
        caching_function(i)


if __name__ == '__main__':
    simple_function()
    simple_function()
    simple_function2()
    test_caching_function()
