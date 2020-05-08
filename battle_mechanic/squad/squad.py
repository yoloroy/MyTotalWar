from battle_mechanic.minion.minion import Minion
from battle_mechanic.abstracts import Positionable, Tickable
from lib.funcs import distance


class Squad(Tickable, Positionable):
    SPACING = 2
    rushing = False
    def __init__(self, example: Minion, num, color, enemies=list()):
        self.minions = example * num
        self.enemies = enemies  # enemy squads
        self.color = color

        r, g, b = self.color
        self.minion_color = (
            0xff if r + 0x44 > 0xff else r + 0x44,
            0xff if g + 0x44 > 0xff else g + 0x44,
            0xff if b + 0x44 > 0xff else b + 0x44
        )

    @property
    def position(self):
        return (
            int(sum(map(lambda minion: minion.position[0], self.minions)) / len(self.minions)),
            int(sum(map(lambda minion: minion.position[1], self.minions)) / len(self.minions))
        )

    def rush(self):
        for i in self.minions:
            if i.enemy is None:
                i.choose_enemy(self.enemies)
                i.fight = True

    def line_up(self, xy1, xy2):
        length = int(distance(xy1, xy2) / self.SPACING)

        vector = (
            (xy2[0] - xy1[0]) / length,
            (xy2[1] - xy1[1]) / length
        )

        for i in self.minions:
            i.enemy = None

        for line in range(len(self.minions) // length):
            for i in range(length):
                try:
                    self.minions[i + length*line].goto = (
                        xy1[0] + vector[0] * i + vector[1] * line,
                        xy1[1] + vector[1] * i + vector[0] * line
                    )
                except IndexError:
                    return

    def tick(self, tick):
        if self.rushing:
            self.rush()
        self.minions = list(filter(lambda i: i.tick(tick), self.minions))
        self.enemies = list(filter(lambda i: i.health > 0, self.enemies))

        return bool(len(self.minions))

    def go(self): pass
