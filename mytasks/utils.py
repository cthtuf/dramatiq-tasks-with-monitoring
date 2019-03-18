"""
This file is just example that you actor methods should be thin and doesn't have to contain a lot of logic
"""

from random import randint


def check_if_odd(x: int) -> bool:
    return x % 2 == 0


def get_big_random_list() -> list:
    return [randint(0, 1000000) for i in range(0, 2000000)]


def get_a_little_bit_bigger(than: int) -> int:
    return than + 1
