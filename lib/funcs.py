import threading
from functools import reduce
from typing import Tuple


def distance(pos1, pos2):
    return (
                   (pos1[0] - pos2[0]) ** 2 +
                   (pos1[1] - pos2[1]) ** 2
           ) ** 0.5


def nearest(me, others):
    return min(others, key=lambda i: distance(me.position, i.position))


def hex_color(color: int) -> Tuple[int, int, int]:
    return color // 256 // 256, \
           color // 256 % 256, \
           color % 256


def normalize_color(r, g, b):
    return (
        0xff if r > 0xff else 0x00 if r < 0x00 else r,
        0xff if g > 0xff else 0x00 if g < 0x00 else g,
        0xff if b > 0xff else 0x00 if b < 0x00 else b
    )


def new_thread(func):
    def wrapper(*args):
        thread = threading.Thread(target=func, args=args)
        thread.start()

    return wrapper


def list_sum(array):
    return reduce(lambda a, b: list(a) + list(b), array)


def sign(num):
    return -1 if num < 0 else 1
