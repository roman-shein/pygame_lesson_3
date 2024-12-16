import pygame


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



if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption('Поле')
    size = width, height = 800, 400
    screen = pygame.display.set_mode(size)

    board = Board(10, 6)
    board.set_view(100, 50, 50)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.get_click(event.pos)
        screen.fill((0, 0, 0))
        board.render(screen)
        pygame.display.flip()

    pygame.quit()
