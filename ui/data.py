from dataclasses import dataclass
from typing import List

GRAVITY_TOP = 1
GRAVITY_BOTTOM = 2
GRAVITY_LEFT = 4
GRAVITY_RIGHT = 8
GRAVITY_CENTER = 16

@dataclass
class Margins:
    top: int
    bottom: int
    left: int
    right: int

    def calculate(self, x1, y1, x2, y2) -> List[int]:
        return [self.left + min(x1, x2),
                self.top + min(y1, y2),
                self.right + max(x1, x2),
                self.bottom + max(y1, y2)]
