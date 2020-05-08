from dataclasses import dataclass
from random import random, randint, uniform

import time

from battle_mechanic.abstracts import Tickable, Positionable, Position, MinMax
from lib.funcs import nearest, distance


@dataclass
class Minion(Tickable, Positionable):
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
    enemy = None  # type: Minion

    # temp variables
    fight = False
    goto: Position = None  # coords
    chill_end = None

    def tick(self, tick):
        """Base unit tick mechanic

        :param tick: float, time from last tick
        :return: is the object alive
        """
        if self.health <= 0:
            return False

        if self.chill_end is None or self.chill_end >= time.monotonic():
            self.chill_end = None

            if self.fight and self.enemy is not None:
                self.charge()
                if self.enemy.health <= 0:
                    self.enemy = None
            if self.goto is not None: self.go(tick)

        return True

    def choose_enemy(self, enemies: list):
        """Choose nearest enemy, if enemy exists"""
        try:
            self.enemy = nearest (
                self,
                enemies
            )
        except ValueError:
            return

    # noinspection PyAttributeOutsideInit
    def go(self, tick=1000):
        """Do one tick of move"""
        dx, dy = (self.goto[i] - self.position[i] for i in range(2))
        dist = distance(self.position, self.goto)

        if dist < 1:
            self.goto = None
            return

        self.position = (
            self.position[0] + self.speed * tick * dx / dist,
            self.position[1] + self.speed * tick * dy / dist
        )

    def charge(self):
        """Do one tick of fight"""
        if distance(self.position, self.enemy.position) > self.range:
            self.goto = self.enemy.position
        else:
            self.hit()
            self.chill_end = time.monotonic() + uniform(*self.chill)

    def hit(self):
        """Base hitting mechanic

        work if we didn't miss
        """
        if random() > self.miss:
            self.enemy.receive(randint(*self.damage), self.pierce)

    def receive(self, damage, pierce):
        """Base receive hit mechanic

        work if we didn't dodge or block
        """
        if random() > self.dodging:
            block = self.armor - pierce
            if block < 0:
                block = 0

            damage = damage - block
            if damage > 0:
                self.health -= damage

    def __mul__(self, other):
        if type(other) is int:
            return [self.copy() for _ in range(other)]
        raise ValueError("int required")

    def copy(self):
        """Create full copy of current object"""
        return Minion (
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
