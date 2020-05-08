from typing import Tuple, Union, List

from lib.funcs import hex_color, normalize_color

Position = Union[List[int, int], Tuple[int, int], None]

MinMax = Union[List[int, int], Tuple[int, int]]  # or Iterable[int, int]. Use what you want.

class Tickable:
    def tick(self, tick) -> bool:
        """Logic evaluating

        :returns is the object alive: bool
        :type tick: float
        """

class Positionable:
    position: Position
