from multiprocessing.pool import rebuild_exc
from urllib.parse import scheme_chars

import pygame

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Движущийся круг 2')
    size = width, height = 300, 300
    screen = pygame.display.set_mode(size)

    running = True
    screen.fill((0, 0, 0))
    do_paint = False
    pygame.draw.rect(screen, "green", (0, 0, 100, 100))
    rect_pos = (0, 0)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pred_pos = event.pos
                if (rect_pos[0] <= pred_pos[0] <= rect_pos[0] + 100 and
                        rect_pos[1] <= pred_pos[1] <= rect_pos[1] + 100):
                    do_paint = True
            if event.type == pygame.MOUSEMOTION:
                cur_pos = event.pos
                if do_paint:
                    screen.fill("black")
                    rect_pos = (rect_pos[0] + cur_pos[0] - pred_pos[0],
                                rect_pos[1] + cur_pos[1] - pred_pos[1])
                    pygame.draw.rect(screen, "green", (*rect_pos, 100, 100))
                    pred_pos = cur_pos
            if event.type == pygame.MOUSEBUTTONUP:
                do_paint = False

        pygame.display.flip()
    pygame.quit()
