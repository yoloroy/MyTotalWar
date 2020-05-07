import threading


def sq_distance(pos1, pos2):
    return \
        (pos1[0] - pos2[0]) ** 2 + \
        (pos1[1] - pos2[0]) ** 2


def nearest(pos, poss):
    return min(poss, key=lambda i: sq_distance(pos, i))


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
