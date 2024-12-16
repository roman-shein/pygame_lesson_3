import pygame
from random import randrange

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Движущийся круг 2')
    size = width, height = 800, 400
    screen = pygame.display.set_mode(size)

    running = True
    # v = 100
    clock = pygame.time.Clock()
    screen.fill("black")
    r = 10
    # arr = [[x, y, c, dx, dy, v]]
    arr = []
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                c = (randrange(256), randrange(256), randrange(256))
                dx, dy = -1, -1
                v = randrange(10, 100)
                arr.append([x, y, c, dx, dy, v])
        screen.fill("black")
        t = clock.tick()
        for i in range(len(arr)):
            x, y, c, dx, dy, v = arr[i]
            pygame.draw.circle(screen, c, (int(x), int(y)), r)
            x += dx * v / 1000 * t
            y += dy * v / 1000 * t
            if x - r <= 0:
                dx = 1
                x = r
            if y - r <= 0:
                dy = 1
                y = r
            if x + r >= width:
                dx = -1
                x = width - r
            if y + r >= height:
                dy = -1
                y = height - r
            arr[i] = [x, y, c, dx, dy, v]

        pygame.display.flip()
    pygame.quit()
