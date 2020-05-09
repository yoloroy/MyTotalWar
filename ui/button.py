from dataclasses import dataclass
from typing import Tuple, List, Union

from pygame.surface import Surface
import pygame

from ui.data import GRAVITY_LEFT, GRAVITY_TOP, Margins, GRAVITY_CENTER, GRAVITY_RIGHT, GRAVITY_BOTTOM
from ui.rounded_rect import generate_rounded_rect


@dataclass
class Button:
    surface: Surface
    gravity: int
    background_color: Tuple[int, int, int]
    text: str
    text_color: Tuple[int, int, int]
    on_click_listener: object  # type: function
    radius: int
    margins: Margins

    def __post_init__(self):
        foreground_text = \
            pygame.font.SysFont("Roboto", 20)\
                .render(self.text, True, self.text_color)

        self.width = foreground_text.get_width() + 10
        self.height = foreground_text.get_height() + 8

        self.recalculate()
        self.background.blit(foreground_text, (self.margins.left, self.margins.top))

    def draw(self):
        coords = self.coords.copy()

        # TODO: do nicely
        if self.gravity & GRAVITY_RIGHT:
            coords[0] -= self.margins.left + self.margins.right

        if self.gravity & GRAVITY_BOTTOM:
            coords[1] -= self.margins.top + self.margins.bottom

        self.surface.blit(self.background, coords[0:2])

    def on_click(self, x, y):
        if (x, y) in self and self.on_click_listener is not None:
            # noinspection PyCallingNonCallable
            self.on_click_listener(self)

    # noinspection PyAttributeOutsideInit
    def recalculate(self):
        self.base_coords = self.__base_coords__

        self.coords = self.margins.calculate(*self.base_coords)

        self.background = generate_rounded_rect(self.background_color, self.width, self.height, self.radius)

    @property
    def __base_coords__(self) -> Union[Tuple[int, int, int, int], List[int]]:
        xy1 = [0, 0]
        if self.gravity & GRAVITY_CENTER:
            xy1 = [
                (self.surface.get_width() - self.width) / 2,
                (self.surface.get_height() - self.height) / 2
            ]

        if self.gravity & GRAVITY_LEFT:
            xy1[0] = 0
        elif self.gravity & GRAVITY_RIGHT:
            xy1[0] = self.surface.get_width() - self.width

        if self.gravity & GRAVITY_TOP:
            xy1[1] = 0
        elif self.gravity & GRAVITY_BOTTOM:
            xy1[1] = self.surface.get_height() - self.height

        # noinspection PyTypeChecker
        return [*xy1, xy1[0] + self.width, xy1[1] + self.height]

    def __contains__(self, xy):
        return self.base_coords[0] <= xy[0] <= self.base_coords[2] and \
               self.base_coords[1] <= xy[1] <= self.base_coords[3]
