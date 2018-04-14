# -*- coding:UTF-8 -*-
import pygame

'''
@param top_lift: 左上角的像素坐标位置
@param size: 栅格横竖的切分份数
@param unit_len: 栅格单元的像素大小
@param color: 栅格的边颜色
'''
class Grid:
    def __init__(self, top_left, size_w, size_h, unit_len, color=(0x00, 0x80, 0xff)):
        self.size_w = size_w
        self.size_h = size_h
        self.top_x, self.top_y = top_left
        self.unit_len = unit_len
        self.width = unit_len * size_w
        self.height = unit_len * size_h
        self.color = color

    # 绘制网格边
    def draw_grid_line(self, surface):
        # pygame.draw.line(surface, self.color, (self.top_x, self.top_y), (self.top_x, self.top_y + 100))

        start_y = self.top_y
        end_y = start_y + self.height
        for i in range(0, self.size_w + 1):
            start_x = self.top_x + i * self.unit_len
            end_x = start_x
            pygame.draw.line(surface, self.color, (start_x, start_y), (end_x, end_y))

        start_x = self.top_x
        end_x = start_x + self.width
        for j in range(0, self.size_h + 1):
            start_y = self.top_y + j * self.unit_len
            end_y = start_y
            pygame.draw.line(surface, self.color, (start_x, start_y), (end_x, end_y))

    # 设置单元格长度（最小1）
    def set_unit_len(self, unit_len):
        self.unit_len = unit_len

    # 设置单元格横纵单元格个数
    def set_grid_size(self, size_w, size_h):
        self.size_w = size_w
        self.size_h = size_h
        self.width = self.unit_len * size_w
        self.height = self.unit_len * size_h

    # pos为网格中的坐标位置（0，0）表示第一个单元格
    def draw_unit_grid(self, surface, pos, color=(0, 0, 0)):
        if pos[0] < 0 or pos[1] < 0 \
                or pos[0] > self.size_w - 1 or pos[1] > self.size_h - 1:
            return
        grid_rect = self.get_grid_block_by_grid_pos(pos)
        pygame.draw.rect(surface, color, grid_rect, 0)

    # 根据实际像素位置获取对应栅格的区域rect
    def get_grid_block(self, point):
        relate_x = point[0] - self.top_x
        relate_y = point[1] - self.top_y
        if relate_x < 0:
            relate_x = 0
        if relate_x > self.width:
            relate_x = self.width
        if relate_y < 0:
            relate_y = 0
        if relate_y > self.height:
            relate_y = self.height

        pos_x = self.top_x + (int)(relate_x / self.unit_len) * self.unit_len
        pos_y = self.top_y + (int)(relate_y / self.unit_len) * self.unit_len

        return (pos_x, pos_y, self.unit_len, self.unit_len)

    # 根据像素位置返回栅格的坐标系的点位置
    def get_grid_pos(self, point):
        relate_x = point[0] - self.top_x
        relate_y = point[1] - self.top_y
        if relate_x < 0:
            relate_x = 0
        if relate_x > self.width:
            relate_x = self.width
        if relate_y < 0:
            relate_y = 0
        if relate_y > self.height:
            relate_y = self.height

        return ((int)(relate_x / self.unit_len), (int)(relate_y / self.unit_len))

    # 根据栅格的局部坐标获取画布的像素坐标的区域rect
    def get_grid_block_by_grid_pos(self, grid_pos):
        pos_x = self.top_x + grid_pos[0] * self.unit_len
        pos_y = self.top_y + grid_pos[1] * self.unit_len
        return (pos_x + 1, pos_y + 1, self.unit_len - 1, self.unit_len - 1)