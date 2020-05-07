from BattleMechanic.Minion.Minion import Minion
from Funcs.Funcs import sq_distance, new_thread


class Squad:
    SPACING = 2
    def __init__(self, example: Minion, num, color, enemies=list()):
        self.minions = example.multiply(num)
        self.enemies = enemies  # enemy squads
        self.color = color

        r, g, b = self.color
        self.minion_color = (
            0xff if r + 0xaa > 0xff else r + 0xaa,
            0xff if g + 0xaa > 0xff else g + 0xaa,
            0xff if b + 0xaa > 0xff else b + 0xaa
        )

    @property
    def position(self):
        return (
            int(sum(map(lambda minion: minion.position[0], self.minions)) / len(self.minions)),
            int(sum(map(lambda minion: minion.position[1], self.minions)) / len(self.minions))
        )

    def rush(self):
        for i in self.minions:
            i.choose_enemy(*self.enemies)
            i.fight()

    @new_thread
    def line_up(self, xy1, xy2):
        length = int((sq_distance(xy1, xy2) / self.SPACING) ** 0.5)

        vector = (
            (xy2[0] - xy1[0]) / length,
            (xy2[1] - xy1[1]) / length
        )

        for i in self.minions:
            i.enemy = None

        # size = sum(map(lambda minion: int(minion.health > 0), self.minions))
        for line in range(len(self.minions) // length):
            for i in range(length):
                try:
                    self.minions[i + length*line].go (
                        xy1[0] + vector[0] * i + vector[1] * line,
                        xy1[1] + vector[1] * i + vector[0] * line
                    )
                except IndexError:
                    return
        print(self.color)

    def go(self): pass