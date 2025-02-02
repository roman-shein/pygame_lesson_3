import pygame


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * self.width for _ in range(self.height)]

        self.left = 10
        self.top = 10
        self.cell_size = 50

        self.cur_player = 1

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def draw_board(self):
        for row in range(self.height):
            for col in range(self.width):
                if self.board[row][col] == 1:
                    pygame.draw.line(screen, "blue", (self.left + col * self.cell_size + 4,
                                                      self.top + row * self.cell_size + 4),
                                     (self.left + (col + 1) * self.cell_size - 6,
                                      self.top + (row + 1) * self.cell_size - 6), width=2)
                    pygame.draw.line(screen, "blue", (self.left + col * self.cell_size + 4,
                                                      self.top + (row + 1) * self.cell_size - 6),
                                     (self.left + (col + 1) * self.cell_size - 6,
                                      self.top + row * self.cell_size + 4), width=2)
                elif self.board[row][col] == 2:
                    pygame.draw.circle(screen, "red", (self.left + col * self.cell_size + self.cell_size // 2,
                                                       self.top + row * self.cell_size + self.cell_size // 2),
                                       self.cell_size // 2 - 4, width=2)

                pygame.draw.rect(screen, "white", (self.left + col * self.cell_size,
                                                   self.top + row * self.cell_size,
                                                   self.cell_size, self.cell_size), width=1)

    def get_cell(self, mouse_pos):
        if (self.left <= mouse_pos[0] <= self.cell_size * self.width + self.left and
                self.top <= mouse_pos[1] <= self.cell_size * self.height + self.top):
            x = (mouse_pos[0] - self.left) // self.cell_size
            y = (mouse_pos[1] - self.top) // self.cell_size
            return x, y
        return None

    def on_click(self, cell_coords):
        if cell_coords:
            col, row = cell_coords
            if self.board[row][col] == 0:
                self.board[row][col] = self.cur_player
                self.cur_player = 1 if self.cur_player == 2 else 2

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)


if __name__ == "__main__":
    pygame.init()
    size = width, height = 800, 400
    screen = pygame.display.set_mode(size)

    board = Board(10, 6)
    board.set_view(100, 50, 50)

    running = True

    while running:
        screen.fill("black")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.get_click(event.pos)

        board.draw_board()
        pygame.display.flip()

    pygame.quit()
