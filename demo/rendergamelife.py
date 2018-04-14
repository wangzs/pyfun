# -*- coding:UTF-8 -*-

from algorithm.gamelife import GameLife
from draw.render import BaseRender
from draw.grid import Grid
from utils.logger import WLog
from draw import render

import pygame
import math

base_life_shape = {
    "Glider": [[1,0], [2,1], [2,2], [1,2], [0,2]],
    "Small Exploder": [[0,1], [0,2], [1,0], [1,1], [1,3], [2,1], [2,2]],
    "Exploder": [[0,0], [0,1], [0,2], [0,3], [0,4], [2,0], [2,4], [4,0], [4,1], [4,2], [4,3], [4,4]],
    "10 Cell Row": [[0,0], [1,0], [2,0], [3,0], [4,0], [5,0], [6,0], [7,0], [8,0], [9,0]],
    "Lightweight spaceship": [[0,1], [0,3], [1,0], [2,0], [3,0], [3,3], [4,0], [4,1], [4,2]],
    "Tumbler": [[0,3], [0,4], [0,5], [1,0], [1,1], [1,5], [2,0], [2,1], [2,2], [2,3], [2,4], [4,0], [4,1], [4,2], [4,3], [4,4], [5,0], [5,1], [5,5], [6,3], [6,4], [6,5]],
    "Gosper Glider Gun": [[0,2], [0,3], [1,2], [1,3], [8,3], [8,4], [9,2], [9,4], [10,2], [10,3], [16,4], [16,5], [16,6], [17,4], [18,5], [22,1], [22,2], [23,0], [23,2], [24,0], [24,1], [24,12], [24,13], [25,12], [25,14], [26,12], [34,0], [34,1], [35,0], [35,1], [35,7], [35,8], [35,9], [36,7], [37,8]]
}

MAX_GRID_UNIT = 40
MIX_GRID_UNIT = 3

CHOSE_SHAPE_NAME = "Gosper Glider Gun"

class RenderGameLife(BaseRender):
    def __init__(self, color):
        BaseRender.__init__(self, "Game Life Demo")
        self.color = color
        self.line_grid_unit = 20

        size_w = (int)(math.ceil(self.width / self.line_grid_unit))
        size_h = (int)(math.ceil(self.height / self.line_grid_unit))
        max_w = (int)(self.width / MIX_GRID_UNIT + 2)
        max_h = (int)(self.height / MIX_GRID_UNIT + 2)
        self.grid = Grid((0, 0), size_w, size_h, self.line_grid_unit)
        self.game_life = GameLife(size_w, size_h, max_w, max_h)
        self.run_state = False

    # 获取生命游戏的原始形状信息
    def __get_shape(self, shape_name, delta_pos):
        shape = base_life_shape[shape_name]
        return [[pos[0]+delta_pos[0], pos[1]+delta_pos[1]] for pos in shape]

    def __callback(self, pos, alive):
        if alive:
            self.grid.draw_unit_grid(self.screen, pos, self.color)

    def __change_size(self):
        size_w, size_h, max_w, max_h = self.__get_size()
        self.grid.set_unit_len(self.line_grid_unit)
        self.grid.set_grid_size(size_w, size_h)
        self.game_life.update_size(size_w, size_h, max_w, max_h)

    def __resize(self, is_up):
        if is_up:
            self.line_grid_unit = self.line_grid_unit + 1 if self.line_grid_unit < MAX_GRID_UNIT else MAX_GRID_UNIT
        else:
            self.line_grid_unit = self.line_grid_unit - 1 if self.line_grid_unit > MIX_GRID_UNIT else MIX_GRID_UNIT
        self.__change_size()

    def __get_size(self):
        size_w = (int)(math.ceil(self.width / self.line_grid_unit))
        size_h = (int)(math.ceil(self.height / self.line_grid_unit))
        max_w = (int)(self.width / MIX_GRID_UNIT + 2)
        max_h = (int)(self.height / MIX_GRID_UNIT + 2)
        return size_w, size_h, max_w, max_h

    def on_window_resize(self):
        WLog.d("window size: %d,%d" % (self.width, self.height))
        self.__change_size()

    def render_frame(self):
        BaseRender.clear_bg(self)
        BaseRender.draw_transparent_bg(self)
        self.grid.draw_grid_line(BaseRender.get_surface(self))

        if self.run_state:
            self.game_life.iterate()
        self.game_life.run(self.__callback)

        BaseRender.update(self)

    def on_key_event(self, key_code, is_down):
        if key_code == pygame.K_SPACE and is_down:
            self.run_state = not self.run_state

    def on_mouse_event(self, mouse_event, is_down):
        if mouse_event == render.MOUSE_SCROLL_UP:
            self.__resize(True)
        elif mouse_event == render.MOUSE_SCROLL_DOWN:
            self.__resize(False)
        elif mouse_event == render.MOUSE_LEFT_BUTTON and is_down:
            pix_pos = pygame.mouse.get_pos()
            WLog.d("mouse click pos: %d,%d" % (pix_pos[0], pix_pos[1]))
            grid_pos = self.grid.get_grid_pos(pix_pos)
            WLog.d("grid pos: %d,%d" % (grid_pos[0], grid_pos[1]))
            self.game_life.set_origin(self.__get_shape(CHOSE_SHAPE_NAME, grid_pos))


WLog.enable = False
game_life = RenderGameLife((0x00, 0x00, 0x00))
game_life.start()