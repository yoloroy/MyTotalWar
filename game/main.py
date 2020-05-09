import pygame

import time

from battle_mechanic.minion.melee.example import example
from battle_mechanic.squad.squad import Squad
from lib.funcs import hex_color, list_sum, new_thread
from ui.button import Button
from ui.data import GRAVITY_LEFT, GRAVITY_TOP, Margins, GRAVITY_RIGHT, GRAVITY_CENTER, GRAVITY_BOTTOM

running = True
pygame.init()
size = width, height = 400, 300
fps = 30
clock = pygame.time.Clock()
surface = pygame.display.set_mode(size)

reds = []

blues = []


@new_thread
def logic(commands):
    """Do game logic mechanics

    all tickables here are Squads because all based on them
    in future be based on Players
    """
    tick = time.monotonic()
    while running:
        tickables = list(filter(lambda x: x.tiick(tick), tickables))
        for i in tickables:
            i.tick(time.monotonic() - tick)
        tick = time.monotonic()


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


def draw():
    """"""

def on_click_chaos(_: Button):
    for i in range(3):
        reds[i].rushing = True
        blues[i].rushing = True


def main():
    global running, reds, blues


    reds = [
        Squad(example((100, 150)), 300, hex_color(0xff0000)),
        Squad(example((100, 150)), 200, hex_color(0xbb4400)),
        Squad(example((100, 150)), 200, hex_color(0xbb0044))
    ]

    blues = [
        Squad(example((300, 150)), 300, hex_color(0x0000ff)),
        Squad(example((300, 150)), 200, hex_color(0x0044bb)),
        Squad(example((300, 150)), 200, hex_color(0x4400bb))
    ]

    for i in range(3):
        reds[i].enemies = [*list_sum(j.minions for j in blues)]
        blues[i].enemies = [*list_sum(j.minions for j in reds)]

    reds[0].line_up((85, 200), (85, 100))
    reds[1].line_up((100, 270), (100, 220))
    reds[2].line_up((100, 80), (100, 30))

    blues[0].line_up((315, 100), (315, 200))
    blues[1].line_up((300, 220), (300, 270))
    blues[2].line_up((300, 30), (300, 80))


    rush_button = Button(
        surface,
        GRAVITY_CENTER,
        hex_color(0xdddddd),
        "Run chaos",
        hex_color(0x181818),
        on_click_chaos,
        4,
        Margins(5, 5, 5, 5))

    while running:
        surface.fill(hex_color(0x000000))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                rush_button.on_click(*pygame.mouse.get_pos())

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

        rush_button.draw()

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