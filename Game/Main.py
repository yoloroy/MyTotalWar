import pygame

from BattleMechanic.Minion.Melee.Example import Example
from BattleMechanic.Squad.Squad import Squad
from Funcs.Funcs import hex_color


def draw_minions(surface, squad):
    for i in squad.minions:
        pygame.draw.line(
            surface,
            squad.minion_color,
            i.position,
            i.position
        )


def main():
    pygame.init()
    size = 1000, 700
    surface = pygame.display.set_mode(size)

    running = True

    squad1 = Squad(Example((200, 350)), 100, hex_color(0xff0000))
    squad2 = Squad(Example((800, 350)), 100, hex_color(0x0000ff))
    print("squads")

    squad1.enemies += [squad2]
    squad2.enemies += [squad1]
    print("squads.enemies")

    squad1.line_up((200, 320), (200, 380))
    squad2.line_up((800, 380), (800, 320))
    print("squads line up")

    while running:
        pygame.display.update()
        surface.fill(hex_color(0x000000))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # TODO: remove draw to Player
        draw_minions(surface, squad1)
        draw_minions(surface, squad2)

        #pygame.draw.circle(surface, squad1.color, squad1.position, 2)
        #pygame.draw.circle(surface, squad2.color, squad2.position, 2)




if __name__ == '__main__':
    main()