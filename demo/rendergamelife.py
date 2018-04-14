# -*- coding:UTF-8 -*-

from algorithm.gamelife import GameLife
from draw.render import BaseRender
from draw.grid import Grid
from utils.logger import WLog

import pygame

base_life_shape = {
    "Glider": [[1,0], [2,1], [2,2], [1,2], [0,2]],
    "Small Exploder": [[0,1], [0,2], [1,0], [1,1], [1,3], [2,1], [2,2]],
    "Exploder": [[0,0], [0,1], [0,2], [0,3], [0,4], [2,0], [2,4], [4,0], [4,1], [4,2], [4,3], [4,4]],
    "10 Cell Row": [[0,0], [1,0], [2,0], [3,0], [4,0], [5,0], [6,0], [7,0], [8,0], [9,0]],
    "Lightweight spaceship": [[0,1], [0,3], [1,0], [2,0], [3,0], [3,3], [4,0], [4,1], [4,2]],
    "Tumbler": [[0,3], [0,4], [0,5], [1,0], [1,1], [1,5], [2,0], [2,1], [2,2], [2,3], [2,4], [4,0], [4,1], [4,2], [4,3], [4,4], [5,0], [5,1], [5,5], [6,3], [6,4], [6,5]],
    "Gosper Glider Gun": [[0,2], [0,3], [1,2], [1,3], [8,3], [8,4], [9,2], [9,4], [10,2], [10,3], [16,4], [16,5], [16,6], [17,4], [18,5], [22,1], [22,2], [23,0], [23,2], [24,0], [24,1], [24,12], [24,13], [25,12], [25,14], [26,12], [34,0], [34,1], [35,0], [35,1], [35,7], [35,8], [35,9], [36,7], [37,8]]
}

class RenderGameLife(BaseRender):
    def __init__(self, color):
        BaseRender.__init__(self, "Game Life Demo")
        self.color = color
        self.line_grid_unit = 20
        size = (int)(self.width/ self.line_grid_unit)
        self.grid = Grid((0, 0), size, self.line_grid_unit)
        self.game_life = GameLife(size, size)
        self.run_state = False

    # 获取生命游戏的原始形状信息
    def __get_shape(self, shape_name, delta_pos):
        shape = base_life_shape[shape_name]
        return [[pos[0]+delta_pos[0], pos[1]+delta_pos[1]] for pos in shape]

    def __callback(self, pos, alive):
        if alive:
            self.grid.draw_unit_grid(self.screen, pos, self.color)

    def render_frame(self):
        BaseRender.clear_bg(self)
        BaseRender.draw_transparent_bg(self)
        self.grid.draw_grid_line(BaseRender.get_surface(self))

        if self.run_state:
            self.game_life.iterate()
        self.game_life.run(self.__callback)

        BaseRender.update(self)

    def handle_event(self, event):
        BaseRender.handle_event(self, event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.run_state = not self.run_state
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pix_pos = pygame.mouse.get_pos()
            WLog.d("mouse click pos: %d,%d" % (pix_pos[0], pix_pos[1]))
            grid_pos = self.grid.get_grid_pos(pix_pos)
            WLog.d("grid pos: %d,%d" % (grid_pos[0], grid_pos[1]))
            self.game_life.set_origin(self.__get_shape("Glider", grid_pos))


WLog.enable = True
game_life = RenderGameLife((0x00, 0x00, 0x00))
game_life.start()