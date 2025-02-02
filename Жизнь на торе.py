import pygame
from copy import deepcopy
from random import random


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for row in range(self.height):
            for col in range(self.width):
                if self.board[row][col] == 0:
                    pygame.draw.rect(screen, "white",
                                     (self.left + col * self.cell_size,
                                      self.top + row * self.cell_size,
                                      self.cell_size, self.cell_size), width=1)
                else:
                    pygame.draw.rect(screen, "white",
                                     (self.left + col * self.cell_size,
                                      self.top + row * self.cell_size,
                                      self.cell_size, self.cell_size))

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def get_cell(self, mouse_pos):
        if (self.left <= mouse_pos[0] <= self.cell_size * self.width + self.left and
                self.top <= mouse_pos[1] <= self.cell_size * self.height + self.top):
            x = (mouse_pos[0] - self.left) // self.cell_size
            y = (mouse_pos[1] - self.top) // self.cell_size
            return x, y
        return None

    def on_click(self, cell_coords):
        if cell_coords:
            c, r = cell_coords
            for row in range(self.height):
                self.board[row][c] = (self.board[row][c] + 1) % 2
            for col in range(self.width):
                self.board[r][col] = (self.board[r][col] + 1) % 2
            self.board[r][c] = abs(-1 + self.board[r][c])


class Life(Board):
    def __init__(self, width, height):
        super().__init__(width, height)
        # self.board = [[1 if random() < 0.15 else 0 for __ in range(width)] for _ in range(height)]

    def render(self, screen):
        for row in range(self.height):
            for col in range(self.width):
                if self.board[row][col] == 0:
                    pygame.draw.rect(screen, "white",
                                     (self.left + col * self.cell_size,
                                      self.top + row * self.cell_size,
                                      self.cell_size, self.cell_size), width=1)
                else:
                    pygame.draw.rect(screen, "green",
                                     (self.left + col * self.cell_size,
                                      self.top + row * self.cell_size,
                                      self.cell_size, self.cell_size))

    def on_click(self, cell_coords):
        if cell_coords:
            c, r = cell_coords
            self.board[r][c] = abs(-1 + self.board[r][c])

    def next_move(self):
        t = deepcopy(self.board)
        for row in range(self.height):
            for col in range(self.width):
                if (self.count_cells(row, col) == 3 and self.board[row][col] == 0 or
                        2 <= self.count_cells(row, col) <= 3 and self.board[row][col] == 1):
                    t[row][col] = 1
                else:
                    t[row][col] = 0

        self.board = deepcopy(t)

    def count_cells(self, row, col):
        d = ((-1, -1), (-1, 0), (-1, 1),
             (0, -1), (0, 1),
             (1, -1), (1, 0), (1, 1))
        count = 0
        for dr, dc in d:
            if row + dr >= self.height and col + dc >= self.width:
                count += self.board[0][0]
            elif row + dr >= self.height:
                count += self.board[0][col + dc]
            elif col + dc >= self.width:
                count += self.board[row + dr][0]
            else:
                count += self.board[row + dr][col + dc]
        return count


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption('Поле')
    size = width, height = 800, 800
    screen = pygame.display.set_mode(size)

    life = Life(50, 50)
    life.set_view(10, 10, 15)

    running = True
    fps = 5
    clock = pygame.time.Clock()
    game_on = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                life.get_click(event.pos)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_on = not game_on
        screen.fill((0, 0, 0))
        life.render(screen)
        if game_on:
            life.next_move()
        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()
