import pygame

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Движущийся круг 2')
    size = width, height = 800, 400
    screen = pygame.display.set_mode(size)

    running = True
    v = 10  # пикселей в секунду
    clock = pygame.time.Clock()
    screen.fill("blue")
    do_paint = False
    r = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                do_paint = True
                screen.fill("blue")
                pos = event.pos
                r = 0
                clock.tick()
        if do_paint:
            pygame.draw.circle(screen, "yellow", pos, r)
            r += v / 1000 * clock.tick()
        pygame.display.flip()
    pygame.quit()

