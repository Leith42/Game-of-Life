import configparser as cp
import sys

import pygame

from classes.Board import Board
from classes.Cell import Cell
from classes.Color import Color
from classes.Surface import Surface
from classes.Window import Window


class Game:
    def __init__(self):
        pygame.init()  # Initialize PyGame library.
        self.config = cp.ConfigParser()  # Init the config parser.
        self.config.read('config.ini')  # Open the config file.
        pygame.display.set_caption("Conway's Game of Life")  # Set window title.
        pygame.display.set_icon(pygame.image.load("./assets/img/window_icon.png"))  # Set window icon.
        pygame.mouse.set_cursor(*pygame.cursors.diamond)  # Set mouse cursor.
        self.window = Window(self.config)  # Init window.
        self.screen_surface = pygame.display.set_mode((self.window.width, self.window.height))  # Init the main surface.
        self.background = Surface("./assets/img/background.jpg", (0, 0))  # Init the background surface.
        # self.play_button = Surface("./assets/img/play-button.png", (50, self.window))  # Init the play button surface.
        self.board = Board(self.window, self.config)  # Main structure of the game.

    def draw_background(self):
        self.screen_surface.blit(self.background.image, self.background.rect)

    def draw_board(self):
        half_padding = self.board.matrix_padding // 2
        for x in range(0, self.board.width):
            for y in range(0, self.board.height):
                # Get the current cell.
                cell = self.board.structure[y + half_padding][x + half_padding]

                # Pick the color corresponding to the cell state.
                color = Color.LIGHT_GREY if cell.state is Cell.DEAD else Color.BLACK

                # Draw the current cell.
                cell_size = Cell.SIZE + self.board.zoom
                pygame.draw.rect(self.board.surface, Color.WHITE,
                                 (x * cell_size, y * cell_size, cell_size + 2, cell_size + 2))
                rect = pygame.draw.rect(self.board.surface, color,
                                        ((x * cell_size) + 1, (y * cell_size) + 1, cell_size, cell_size))

                # Store the 2D coordinates of the cell on the surface.
                self.board.structure[y + half_padding][x + half_padding].rect = rect
        # Blit the board surface on the screen surface.
        self.screen_surface.blit(self.board.surface,
                                 ((self.window.width - (self.board.width * Cell.SIZE)) >> 1, self.board.h_padding))

    def clear_board(self):
        """
        Clear the board by killing every living cells.
        """
        for y in self.board.structure:
            for x in y:
                x.state = Cell.DEAD

    def process_cell_action(self, click_pos):
        """
        Process the user action on a cell.

        :param click_pos:
        :return:
        """
        for row in self.board.structure:
            for cell in row:
                if cell.rect is not None:
                    if cell.rect.left <= click_pos[0] - self.board.w_padding <= cell.rect.right and \
                            cell.rect.top <= click_pos[1] - self.board.h_padding <= cell.rect.bottom:
                        cell.swap_state()
                        return

    def calculates_cell_next_states(self):
        """
        Calculates and saves the next cell states.
        """
        for y, row in enumerate(self.board.structure):
            for x, cell in enumerate(row):
                neighbors = self.neighbors_counter(x, y)
                if neighbors is 3 and cell.state is Cell.DEAD:
                    cell.save_next_state(Cell.ALIVE)
                if neighbors < 2 or neighbors > 3 and cell.state is Cell.ALIVE:
                    cell.save_next_state(Cell.DEAD)

    def apply_cell_next_states(self):
        for row in self.board.structure:
            for cell in row:
                cell.apply_next_state()

    def neighbors_counter(self, pos_x, pos_y) -> int:
        neighbors = 0
        y_max = self.board.height + self.board.matrix_padding - 1
        x_max = self.board.width + self.board.matrix_padding - 1

        # LEFT
        if pos_x > 0 and self.board.structure[pos_y][pos_x - 1].state is Cell.ALIVE:
            neighbors += 1
        # RIGHT
        if pos_x < x_max and self.board.structure[pos_y][pos_x + 1].state is Cell.ALIVE:
            neighbors += 1
        # UP
        if pos_y > 0 and self.board.structure[pos_y - 1][pos_x].state is Cell.ALIVE:
            neighbors += 1
        # DOWN
        if pos_y < y_max and self.board.structure[pos_y + 1][pos_x].state is Cell.ALIVE:
            neighbors += 1
        # UP LEFT
        if (pos_x > 0 and pos_y > 0) and self.board.structure[pos_y - 1][pos_x - 1].state is Cell.ALIVE:
            neighbors += 1
        # UP RIGHT
        if (pos_x < x_max and pos_y > 0) and self.board.structure[pos_y - 1][pos_x + 1].state is Cell.ALIVE:
            neighbors += 1
        # DOWN LEFT
        if (pos_x > 0 and pos_y < y_max) and self.board.structure[pos_y + 1][pos_x - 1].state is Cell.ALIVE:
            neighbors += 1
        # DOWN RIGHT
        if (pos_x < x_max and pos_y < y_max) and self.board.structure[pos_y + 1][pos_x + 1].state is Cell.ALIVE:
            neighbors += 1
        return neighbors

    def refresh_board(self):
        self.draw_board()
        pygame.display.flip()
        print("Zoom: {}".format(self.board.zoom))

    # def draw_buttons(self):
    #     self.screen_surface.blit(self.play_button.image, self.play_button.rect)

    def run(self):
        pygame.transform.rotate(self.board.surface, 40)
        self.draw_background()
        self.draw_board()
        # self.draw_buttons()
        pygame.display.update()
        idle_mode = True
        while True:
            for event in pygame.event.get():
                if event.type is pygame.QUIT:
                    sys.exit()

                elif event.type is pygame.MOUSEBUTTONUP:
                    if event.button is 1:  # LEFT MOUSE CLICK
                        self.process_cell_action(event.pos)
                        self.refresh_board()
                    elif event.button is 4:  # MOUSE WHEEL UP
                        self.board.zoom_in()
                        self.refresh_board()
                    elif event.button is 5:  # MOUSE WHEEL DOWN
                        self.board.zoom_out()
                        self.refresh_board()

                elif event.type is pygame.KEYUP and event.key is pygame.K_DELETE:  # DEL BUTTON
                    self.clear_board()
                    self.refresh_board()
                    idle_mode = True

                elif event.type is pygame.KEYUP and event.key is pygame.K_SPACE:  # SPACE BUTTON
                    idle_mode = True if idle_mode is False else False

            if idle_mode is False:
                self.calculates_cell_next_states()
                self.apply_cell_next_states()
                self.refresh_board()
