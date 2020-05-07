import threading
from functools import reduce


def sq_distance(pos1, pos2):
    return \
        (pos1[0] - pos2[0]) ** 2 + \
        (pos1[1] - pos2[0]) ** 2


def nearest(me, others):
    return min(others, key=lambda i: sq_distance(me.position, i.position))


def hex_color(color):
    return \
        int(color // 256 // 256), \
        int(color // 256 % 256), \
        int(color % 256)


def new_thread(func):
    def wrapper(*args):
        thread = threading.Thread(target=func, args=args)
        thread.start()

    return wrapper


def list_sum(array):
    return reduce(lambda a, b: list(a) + list(b), array)

def sign(num):
    return -1 if num < 0 else 1
