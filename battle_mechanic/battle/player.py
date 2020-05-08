from dataclasses import dataclass
from typing import List

from battle_mechanic.squad.squad import Squad


@dataclass
class Player:
    squads: List[Squad]
