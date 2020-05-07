from dataclasses import dataclass
from random import random, randint
from typing import Tuple

from Funcs.Funcs import nearest, sq_distance, sign


@dataclass
class Minion:
    position: Tuple[float, float]  # position by (x, y)
    health: int  # health limit
    damage: Tuple[int, int]  # [min, max]
    pierce: int  # value of armor ignore
    armor: int  # value of damage ignore
    dodging: float  # chance of full ignore damage
    miss: float  # chance of missing
    range: int  # melee attack range
    chill: Tuple[int, int]  # time between attacks [min, max]
    speed: int  # tiles per second
    enemy = None  # type: Minion
    fight = False
    goto: Tuple[int, int] = None  # coords

    def tick(self, tick):
        if self.health <= 0:
            return False

        if self.fight and self.enemy is not None:
            self.charge()
            if self.enemy.health <= 0:
                self.enemy = None
        if self.goto is not None: self.go(tick)

        return True

    def choose_enemy(self, enemies: list):
        try:
            self.enemy = nearest (
                self,
                enemies
            )
        except ValueError:
            return

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

    # base hit mechanic
    def hit(self):
        # if we didn't miss
        if random() > self.miss:
            self.enemy.receive(randint(*self.damage), self.pierce, self)

    # base receive hit mechanic
    def receive(self, damage, pierce, enemy=None):
        # if we didn't dodge/block
        if random() > self.dodging:
            block = self.armor - pierce
            if block < 0:
                block = 0

            damage = damage - block
            if damage > 0:
                self.health -= damage

        # if we can hit back
        if sq_distance(self.position, enemy.position) - self.range <= 1 and self.health > 0:
            self.enemy = enemy
            self.charge()

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
