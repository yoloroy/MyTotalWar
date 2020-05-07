from dataclasses import dataclass
from random import random, randint
from typing import Tuple

from math import sin, cos, atan, asin

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
        if self.fight: self.charge()
        if self.goto is not None: self.go(tick)

    def choose_enemy(self, enemies: list):
        self.enemy = nearest (
            self,
            enemies
        )

    def go(self, tick=1000):
        try:
            angle = atan((self.goto[1] - self.position[1]) / (self.goto[0] - self.position[0]))
        except ZeroDivisionError:
            angle = sign(self.goto[1] - self.position[1])
        self.position = \
            (self.position[0] + self.speed * tick * cos(angle),
             self.position[1] + self.speed * tick * sin(angle))

        if sq_distance(self.position, self.goto) < 1:
            self.goto = None

    # start fight
    def charge(self):
        if sq_distance(self.position, self.enemy.position) > self.range ** 2:
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
        if sq_distance(self.position, enemy.position) - self.range ** 2 <= 1:
            self.enemy = enemy
            self.charge()

    def multiply(self, num):
        return [self.copy() for _ in range(num)]

    def copy(self):
        return Minion(
            self.position,
            self.health,
            self.damage,
            self.pierce,
            self.armor,
            self.dodging,
            self.miss,
            self.range,
            self.chill,
            self.speed
        )
