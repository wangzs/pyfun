# -*- coding:UTF-8 -*-
import pygame
# 常用的函数和常量
from pygame.locals import *
from sys import exit
import time


class BaseRender:
    def __init__(self, wnd_title):
        self.bg_color = (255, 255, 255)
        self.grid_unit = 16
        self.width = 800
        self.height = 600
        self.wnd_title = wnd_title
        self.screen = ()
        pygame.init()

    def get_surface(self):
        return self.screen

    def draw_rect_fill(self, rect, color=(0, 0, 0)):
        pygame.draw.rect(self.screen, color, rect, 0)

    def set_bg_color(self, bg_color):
        self.bg_color = bg_color

    def draw_transparent_bg(self):
        len_x = (int)(self.width / self.grid_unit + 0.5)
        len_y = (int)(self.height / self.grid_unit + 0.5)

        for y in range(0, len_y):
            for x in range(0, len_x, 2):
                top_y = y * self.grid_unit
                top_x = (x + (y + 1) % 2) * self.grid_unit
                pygame.draw.rect(self.screen, (0xdc, 0xdc, 0xdc), (top_x, top_y, self.grid_unit, self.grid_unit), 0)

    def set_screen_size(self, w, h):
        self.width = w
        self.height = h

    def on_window_resize(self):
        pass

    def on_before_exit(self):
        pass

    def clear_bg(self):
        self.screen.fill(self.bg_color)

    def update(self):
        pygame.display.update()

    # 子类重新实现该函数即可绘制子类自己的一帧
    def render_frame(self):
        self.clear_bg()
        self.draw_transparent_bg()
        self.update()

    # 子类重新实现函数即可响应设备的输入
    def handle_event(self, event):
        if event.type == KEYDOWN and event.key == K_ESCAPE \
                or event.type == QUIT:
            self.on_before_exit()
            exit()
        elif event.type == VIDEORESIZE:
            self.width = event.w
            self.height = event.h
            self.screen = pygame.display.set_mode((self.width, self.height), RESIZABLE, 32)
            self.on_window_resize()

    def start(self, mode=RESIZABLE):
        self.screen = pygame.display.set_mode((self.width, self.height), mode, 32)
        pygame.display.set_caption(self.wnd_title)

        while True:
            for event in pygame.event.get():
                self.handle_event(event)
            self.render_frame()

            # test = BaseRender("Test Base Render class")
            # test.start()