from typing import Tuple, Union, List

Position = Union[List[int], Tuple[int, int], None]

MinMax = Union[List[int], Tuple[int, int]]  # or Iterable[int, int]. Use what you want.

class Tickable:
    def tick(self, tick) -> bool:
        """Logic evaluating

        :returns is the object alive: bool
        :type tick: float
        """

class Positionable:
    position: Position
