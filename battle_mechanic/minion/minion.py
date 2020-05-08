import time
from dataclasses import dataclass
from random import random, randint, uniform
from typing import Tuple, Union, List

from lib.funcs import nearest, sq_distance

Position = Union[Tuple[int, int], Tuple[int, int], None]
MinMax = Union[List[int, int], Tuple[int, int]]  # or Iterable[int, int]. Use what you want.


@dataclass
class Minion:
    # unit params:
    position: Position  # position by (x, y)
    health: int  # health limit
    damage: MinMax  # [min, max]
    pierce: int  # value of armor ignore
    armor: int  # value of damage ignore
    dodging: float  # chance of full ignore damage
    miss: float  # chance of missing
    range: int  # melee attack range
    chill: MinMax  # time between attacks [min, max]
    speed: int  # tiles per second

    # enemy
    enemy = None  # type: Union[Minion, None]

    # temp variables
    fight: bool = False
    goto: Position = None  # coords
    chill_end = None

    def tick(self, tick):
        # die
        if self.health <= 0:
            return False

        if self.chill_end is None or self.chill_end >= time.monotonic():
            self.chill_end = None

            if self.fight and self.enemy is not None:
                self.charge()
                if self.enemy.health <= 0:
                    self.enemy = None
            if self.goto is not None:
                self.go(tick)

        return True

    def choose_enemy(self, enemies: list):
        try:
            self.enemy = nearest(
                self,
                enemies
            )
        except ValueError:
            return

    # noinspection PyAttributeOutsideInit
    def go(self, tick=1000):
        dx, dy = (self.goto[i] - self.position[i] for i in range(2))
        dist = sq_distance(self.position, self.goto)

        if dist < 1:
            self.goto = None
            return

        self.position = (
            self.position[0] + self.speed * tick * dx / dist,
            self.position[1] + self.speed * tick * dy / dist
        )

    # start fight
    def charge(self):
        if sq_distance(self.position, self.enemy.position) > self.range:
            self.goto = self.enemy.position
        else:
            self.hit()
            self.chill_end = time.monotonic() + uniform(*self.chill)

    # base hit mechanic
    def hit(self):
        # if we didn't miss
        if random() > self.miss:
            self.enemy.receive(randint(*self.damage), self.pierce)

    # base receive hit mechanic
    def receive(self, damage, pierce):
        # if we didn't dodge/block
        if random() > self.dodging:
            block = self.armor - pierce
            if block < 0:
                block = 0

            damage = damage - block
            if damage > 0:
                self.health -= damage

    def multiply(self, num):
        return [self.copy() for _ in range(num)]

    def copy(self):
        return Minion(
            self.position,
            self.health + randint(0, 1),
            [randint(-1, 1) + i for i in self.damage],
            self.pierce,
            self.armor,
            self.dodging,
            self.miss,
            self.range,
            self.chill,
            self.speed
        )
