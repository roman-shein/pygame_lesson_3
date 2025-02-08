import pygame
from random import randint


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


class Minesweeper(Board):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.board = [[-1] * width for _ in range(height)]
        self.mines = []
        for _ in range(10):
            row, col = randint(0, 9), randint(0, 9)
            if (row, col) in self.mines:
                while (row, col) in self.mines:
                    row, col = randint(0, 9), randint(0, 9)
            self.mines.append((row, col))
            self.board[row][col] = 10
        self.rec = []

    def render(self, screen):
        for row in range(self.height):
            for col in range(self.width):
                if self.board[row][col] == 10:
                    pygame.draw.rect(screen, "red",
                                     (self.left + col * self.cell_size,
                                      self.top + row * self.cell_size,
                                      self.cell_size, self.cell_size))
                elif self.board[row][col] != -1:
                    font = pygame.font.Font(None, 50)
                    text = font.render(str(self.board[row][col]), True, (100, 255, 100))
                    text_x = self.left + col * self.cell_size + 5
                    text_y = self.top + row * self.cell_size + 5
                    text_w = text.get_width()
                    text_h = text.get_height()
                    screen.blit(text, (text_x, text_y))
                pygame.draw.rect(screen, "white",
                                 (self.left + col * self.cell_size,
                                  self.top + row * self.cell_size,
                                  self.cell_size, self.cell_size), width=1)

    def open_cell(self, c, r):
        if self.board[r][c] == -1:
            self.rec.append((r, c))
            arr = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
            count = 0
            for row, col in arr:
                if 0 <= r + row < self.width and 0 <= c + col < self.height:
                    if self.board[r + row][c + col] == 10:
                        count += 1

            if count == 0:
                for row, col in arr:
                    if 0 <= r + row < self.width and 0 <= c + col < self.height:
                        if self.board[r + row][c + col] == -1 and (r + row, c + col) not in self.rec:
                            self.open_cell(c + col, r + row)
            self.board[r][c] = count

    def open_empty_cell(self, x, y):
        pass

    def on_click(self, cell_coords):
        if cell_coords:
            self.open_cell(*cell_coords)


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption('Поле')
    size = width, height = 800, 800
    screen = pygame.display.set_mode(size)

    saper = Minesweeper(10, 10)
    saper.set_view(25, 25, 50)

    running = True

    screen.fill("black")
    saper.render(screen)
    pygame.display.flip()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                saper.get_click(event.pos)
                screen.fill("black")
                saper.render(screen)
                pygame.display.flip()

    pygame.quit()
