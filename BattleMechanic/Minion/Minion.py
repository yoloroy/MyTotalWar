import threading
from dataclasses import dataclass
from random import random, randint
from time import sleep, monotonic
from typing import Tuple

from Funcs.Funcs import nearest, sq_distance


@dataclass
class Minion:
    position: Tuple[int, int]  # position by (x, y)
    health: int  # health limit
    damage: Tuple[int, int]  # [min, max]
    pierce: int  # value of armor ignore
    armor: int  # value of damage ignore
    dodging: float  # chance of full ignore damage
    miss: float  # chance of missing
    range: int  # melee attack range
    chill: Tuple[int, int]  # time between attacks [min, max]
    speed: float  # tiles per second
    enemy = None  # type: Minion
    thread_fight = None
    thread_go = None

    def multiply(self, num):
        return [self.copy() for _ in range(num)]

    def choose_enemy(self, enemies: list):
        self.enemy = nearest (
            self.position,
            map(lambda enemy: enemy.position, enemies)
        )

    def go(self, x, y):
        def phase():
            time = monotonic()
            while self.health > 0 or sq_distance(self.position, (x, y)) > 1:
                self.position = \
                    (self.position[0] + self.speed * (monotonic() - time),
                     self.position[1] + self.speed * (monotonic() - time) )
                time = monotonic()

        self.thread_go = threading.Thread(target=phase)
        self.thread_go.start()

    # start fight
    def fight(self):
        def phase():
            while self.enemy is not None and self.health > 0 and self.enemy.health > 0:
                if sq_distance(self.position, self.enemy.position) > self.range ** 2:
                    self.go(*self.enemy.position)
                else:
                    self.hit()
                    sleep(randint(*self.chill))

        self.thread_fight = threading.Thread(target=phase)
        self.thread_fight.start()

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
            self.fight()

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
