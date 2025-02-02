import pygame


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * self.width for _ in range(self.height)]

        self.left = 10
        self.top = 10
        self.cell_size = 50

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def draw_board(self):
        for row in range(self.height):
            for col in range(self.width):
                if self.board[row][col] == 1:
                    pygame.draw.rect(screen, "red", (self.left + col * self.cell_size,
                                                     self.top + row * self.cell_size,
                                                     self.cell_size, self.cell_size), width)
                elif self.board[row][col] == 2:
                    pygame.draw.rect(screen, "blue", (self.left + col * self.cell_size,
                                                      self.top + row * self.cell_size,
                                                      self.cell_size, self.cell_size), width)

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
            self.board[row][col] = (self.board[row][col] + 1) % 3

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
