import pygame

from classes.Cell import Cell


class Board:
    def __init__(self, window, config):
        # Board size is relative to window and cell size.
        self.width = \
            (window.width - ((window.width * config.getint('BOARD', 'WidthReducePercentage')) // 100)) // Cell.SIZE
        self.height = \
            (window.height - ((window.height * config.getint('BOARD', 'HeightReducePercentage')) // 100)) // Cell.SIZE

        print("X axis: {},".format(self.width), "Y axis: {}".format(self.height))
        # Indicates the zoom level
        self.zoom = 0

        # Padding size of the matrix. It's purpose is to make a borderless board.
        self.matrix_padding = 50

        # Padding in pixels between window surface and board surface.
        self.w_padding = (window.width - (self.width * Cell.SIZE)) >> 1
        self.h_padding = 10

        # Pygame surface of the board.
        self.surface = pygame.Surface((self.width * Cell.SIZE + 2, self.height * Cell.SIZE + 2))

        # Initialize the main structure of the game.
        self.structure = self.init_board_structure()

    def zoom_in(self):
        if self.zoom < 20:
            self.zoom += 2

    def zoom_out(self):
        if self.zoom > 0:
            self.zoom -= 2

    def init_board_structure(self) -> list:
        """
        Populate the board structure with dead cells.
        """
        structure = []
        for y in range(0, self.height + self.matrix_padding):
            new = []
            for x in range(0, self.width + self.matrix_padding):
                new.append(Cell(Cell.DEAD, None))
            structure.append(new)
        return structure
