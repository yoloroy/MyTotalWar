import pygame

from BattleMechanic.Minion.Melee.Example import Example
from BattleMechanic.Squad.Squad import Squad
from Funcs.Funcs import hex_color, list_sum



def draw_text(surf, text, size, x, y, color):
    font = pygame.font.Font("18963.ttf", size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def draw_minions(surface, squad):
    for i in squad.minions:
        pygame.draw.line (
            surface,
            squad.minion_color,
            i.position,
            i.position
        )


def main():
    pygame.init()
    size = width, height = 400, 300
    fps = 30
    clock = pygame.time.Clock()
    surface = pygame.display.set_mode(size)

    running = True

    reds = [
        Squad(Example((100, 150)), 300, hex_color(0xff0000)),
        Squad(Example((100, 150)), 200, hex_color(0xbb4400)),
        Squad(Example((100, 150)), 200, hex_color(0xbb0044))
    ]

    blues = [
        Squad(Example((300, 150)), 300, hex_color(0x0000ff)),
        Squad(Example((300, 150)), 200, hex_color(0x0044bb)),
        Squad(Example((300, 150)), 200, hex_color(0x4400bb))
    ]

    for i in range(3):
        reds[i].enemies = [*list_sum(j.minions for j in blues)]
        blues[i].enemies = [*list_sum(j.minions for j in reds)]

    reds[0].line_up(( 85, 200), ( 85, 100))
    reds[1].line_up((100, 270), (100, 220))
    reds[2].line_up((100,  80), (100,  30))

    blues[0].line_up((315, 100), (315, 200))
    blues[1].line_up((300, 220), (300, 270))
    blues[2].line_up((300,  30), (300,  80))

    while running:
        surface.fill(hex_color(0x000000))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(3):
                    reds [i].battle = True
                    blues[i].battle = True

        for i in range(3):
            reds [i].tick(1 / fps)
            blues[i].tick(1 / fps)

        # TODO: remove draw to Player
        for i in range(3):
            draw_minions(surface, reds [i])
            draw_minions(surface, blues[i])

        for i in range(3):
            try:
                pygame.draw.circle(surface, reds[i].color, reds[i].position, 4)
            except ZeroDivisionError: pass
            try:
                pygame.draw.circle(surface, blues[i].color, blues[i].position, 4)
            except ZeroDivisionError: pass

        if sum(len(i.minions) for i in reds) <= 0:
            print("reds loose")
            win = "REDS", 0xee1111
            break
        if sum(len(i.minions) for i in blues) <= 0:
            print("blues loose")
            win = "BLUES", 0x1111ee
            break

        pygame.display.update()
        pygame.display.flip()
        clock.tick(fps)

    surface.fill(hex_color(0x000000))

    draw_text(surface, f"{win[0]}!", 64, width / 2, height / 4, hex_color(win[1]))
    draw_text(surface, "WINS", 22,
              width / 2, height / 2, hex_color(win[1]))
    draw_text(surface, "Press a key to restart", 18, width / 2, height * 3 / 4, hex_color(win[1]))
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                main()


if __name__ == '__main__':
    main()