import pygame
from copy import deepcopy


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


class Lines(Board):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.path = []
        self.moving = False

    def render(self, screen):
        for row in range(self.height):
            for col in range(self.width):
                pygame.draw.rect(screen, "white",
                                 (self.left + col * self.cell_size,
                                  self.top + row * self.cell_size,
                                  self.cell_size, self.cell_size), width=1)

                if self.board[row][col] == 1:  # blue
                    color = "blue"
                elif self.board[row][col] == 2:  # red
                    color = "red"

                if self.board[row][col] > 0:
                    pygame.draw.circle(screen, color,
                                       (self.left + col * self.cell_size + self.cell_size // 2,
                                        self.top + row * self.cell_size + self.cell_size // 2),
                                       self.cell_size // 2 - 1)

    def on_click(self, cell_coords):
        if cell_coords:
            c, r = cell_coords
            if self.board[r][c] == 0:
                res = self.is_found_red_ball()
                if res:
                    if self.has_path(res[0], res[1], r, c):
                        # self.board[res[0]][res[1]] = 0
                        self.moving = True
                        # self.board[r][c] = 1
                else:
                    self.board[r][c] = 1
            elif self.board[r][c] == 1:
                self.board[r][c] = 2
            elif self.board[r][c] == 2:
                self.board[r][c] = 1

    def is_found_red_ball(self):
        for row in range(self.height):
            for col in range(self.width):
                if self.board[row][col] == 2:
                    return row, col
        return None

    def has_path(self, r1, c1, r2, c2):
        t = deepcopy(self.board)
        que = [(r1, c1)]
        t[r1][c1] = -1
        while que:
            r, c = que.pop(0)
            if (r, c) == (r2, c2):
                self.path = [(r2, c2)]
                (r, c) = (r2, c2)
                for i in range(abs(t[r2][c2]) - 1):
                    if r - 1 >= 0 and t[r - 1][c] == t[r][c] + 1:
                        (r, c) = (r - 1, c)
                        self.path.append((r, c))
                        continue
                    if r + 1 < self.height and t[r + 1][c] == t[r][c] + 1:
                        (r, c) = (r + 1, c)
                        self.path.append((r, c))
                        continue
                    if c - 1 >= 0 and t[r][c - 1] == t[r][c] + 1:
                        (r, c) = (r, c - 1)
                        self.path.append((r, c))
                        continue
                    if c + 1 < self.height and t[r][c + 1] == t[r][c] + 1:
                        (r, c) = (r - 1, c + 1)
                        self.path.append((r, c))
                        continue
                self.path.pop(-1)
                return True
            if r - 1 >= 0 and t[r - 1][c] == 0:
                t[r - 1][c] = t[r][c] - 1
                que.append((r - 1, c))
            if r + 1 < self.height and t[r + 1][c] == 0:
                t[r + 1][c] = t[r][c] - 1
                que.append((r + 1, c))
            if c - 1 >= 0 and t[r][c - 1] == 0:
                t[r][c - 1] = t[r][c] - 1
                que.append((r, c - 1))
            if c + 1 < self.height and t[r][c + 1] == 0:
                t[r][c + 1] = t[r][c] - 1
                que.append((r, c + 1))
        return False

    def move_red(self):
        coords = self.is_found_red_ball()
        if coords:
            self.board[coords[0]][coords[1]] = 0
            if self.path:
                r, c = self.path.pop(-1)
                self.board[r][c] = 2
            else:
                self.board[coords[0]][coords[1]] = 1
        else:
            self.moving = False


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption('Поле')
    size = width, height = 800, 400
    screen = pygame.display.set_mode(size)

    lines = Lines(10, 10)
    lines.set_view(10, 10, 30)

    running = True
    clock = pygame.time.Clock()
    fps = 10
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                lines.get_click(event.pos)
        screen.fill((0, 0, 0))
        lines.render(screen)
        if lines.moving:
            lines.move_red()
        clock.tick(fps)
        pygame.display.flip()

    pygame.quit()
