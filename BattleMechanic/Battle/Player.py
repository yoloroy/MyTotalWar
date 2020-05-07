from dataclasses import dataclass
from typing import List

from BattleMechanic.Squad.Squad import Squad


@dataclass
class Player:
    squads: List[Squad]

    pass#ing
