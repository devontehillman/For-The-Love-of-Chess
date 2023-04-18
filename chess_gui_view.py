#!/usr/bin/env python3

import pygame as pg
import pygame_gui as gui
from game import *


class GUI:
    def __init__(self) -> None:
        pg.init()
        self._game = Game()
        Piece._game = self._game
        self._screen = pg.display.set_mode((1440, 900))
        pg.display.set_caption("For The Love of Chess")
        self._pieces = pg.image.load("./images/pieces.png")
        self._ui_manager = gui.UIManager((1440, 900))
        self._side_box = gui.elements.UITextBox('<b>Laker Chess</b><br /><br />White moves first.<br />', relative_rect=pg.Rect((1000, 100), (400, 500)),
                                manager=self._ui_manager)
        self._undo_button = gui.elements.UIButton(relative_rect = pg.Rect((1000, 50), (100, 50)), text='Undo',
                                    manager=self._ui_manager)
        self._restart_button = gui.elements.UIButton(relative_rect = pg.Rect((1200, 50), (100, 50)), text='Reset',
                                    manager=self._ui_manager)
        self._piece_selected = False
        self._first_selected = (0, 0)
        self._second_selected = (0, 0)
        self._valid_moves = []

    def run_game(self) -> None:
        running = True
        time_delta = 0
        clock = pg.time.Clock()
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    x, y = pg.mouse.get_pos()
                    y, x = self.__get_coords__(y, x)
                    piece = self._game.get(y, x)
                    if not self._piece_selected and piece:
                        if piece.color != self._game.current_player:
                            continue
                        self._piece_selected = True
                        self._first_selected = y, x
                        self._valid_moves = piece.valid_moves(y, x)
                        self._piece_selected = piece
                    elif self._piece_selected and (y, x) in self._valid_moves:
                        target = self._game.get(y, x)
                        moved = self._game.move(self._piece_selected, self._first_selected[0], self._first_selected[1], y, x)
                        if moved:
                            self._side_box.append_html_text(self._piece_selected.color.name + ' moved '
                                                + str(type(self._piece_selected).__name__))
                            if target:
                                self._side_box.append_html_text(' and captures ' + str(type(target).__name__))
                            self._side_box.append_html_text('<br />')
                            computer_message = self._game._computer_move()
                            if computer_message:
                                self._side_box.append_html_text(computer_message)
                        else:
                            self._side_box.append_html_text('Invalid move.  Would leave '
                                                            + str(self._piece_selected.color.name) + ' in check.<br />')
                        if self._game.check(Color.WHITE):
                            self._side_box.append_html_text("WHITE is in CHECK!<br />")
                        if self._game.check(Color.BLACK):
                            self._side_box.append_html_text("BLACK is in CHECK!<br />")
                        if self._game.mate(Color.WHITE):
                            self._side_box.append_html_text("WHITE is in CHECKMATE!<br />GAME OVER!")
                        if self._game.mate(Color.BLACK):
                            self._side_box.append_html_text("BLACK is in CHECKMATE!<br />GAME OVER!")

                        self._piece_selected = False
                    else:
                        self._piece_selected = False
                if event.type == gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self._restart_button:
                        self._game.reset()
                        self._side_box.set_text("Game Reset<br />")
                    if event.ui_element == self._undo_button:
                        if self._game.undo():
                            self._side_box.append_html_text('Undoing move.<br />')
                        else:
                            self._side_box.append_html_text('Nothing to undo.<br />')
            self._ui_manager.process_events(event)

            self._screen.fill((255, 255, 255))
            self.__draw_board__()
            self._ui_manager.draw_ui(self._screen)
            self._ui_manager.update(time_delta)

            pg.display.flip()
            time_delta = clock.tick(30) / 1000.0

    def __get_coords__(self, y, x):
        grid_x = x // 105
        grid_y = y // 105
        return grid_y, grid_x

    def __draw_board__(self) -> None:
        count = 0
        color = (255, 255, 255)
        for y in range(0, 8):
            for x in range(0, 8):
                if count % 2 == 0:
                    color = (255, 255, 255)
                else:
                    color = (127, 127, 127)
                count = count + 1
                pg.draw.rect(self._screen, color, pg.rect.Rect(x * 105, y * 105, 105, 105))
                if self._piece_selected and (y, x) == self._first_selected:
                    pg.draw.rect(self._screen, (255, 0, 0), pg.rect.Rect(x * 105, y * 105, 105, 105), 2)
                if self._valid_moves and self._piece_selected and (y, x) in self._valid_moves:
                    pg.draw.rect(self._screen, (0, 0, 255), pg.rect.Rect(x * 105, y * 105, 105, 105), 2)
                if self._game.get(y, x):
                    self._screen.blit(self._game.get(y, x)._image, (x * 105, y * 105))
            count = count + 1
        pg.draw.line(self._screen, (0, 0, 0), (0, 840), (840, 840))
        pg.draw.line(self._screen, (0, 0, 0), (840, 840), (840, 0))


def main():
    g = GUI()
    g.run_game()


if __name__ == '__main__':
    main()
