from typing import Tuple

import pygame
from pygame.draw import circle, polygon


def generate_rounded_rect(color: Tuple[int, int, int], width: int, height: int, radius: int):
    surface = pygame.Surface((width, height))

    for func, args in rounded_rect_coords(width, height, radius):
        func(surface, color, *args)

    return surface


def rounded_rect_coords(width, height, radius):
    return [
        [circle, [[radius, radius], radius]],
        [circle, [[width - radius, radius], radius]],
        [circle, [[radius, height - radius], radius]],
        [circle, [[width - radius, height - radius], radius]],
        [polygon,[[[radius, 0], [width - radius, 0],
                  [width, radius], [width, height - radius],
                  [width - radius, height], [radius, height],
                  [0, height - radius], [0, radius]]]]
    ]