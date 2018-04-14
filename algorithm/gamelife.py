# -*- coding:UTF-8 -*-

from utils.logger import WLog

class GameLife:
    def __init__(self, w, h):
        self.width = w
        self.height = h
        self.world_ceil = [[0 for i in range(w)] for j in range(h)]
        self.alive_life = []
        self.iter_cnt = 0
        WLog.d("w:%d h:%d" % (w, h))

    def update_size(self, w, h):
        # 重置整个世界的单元格
        tmp_world_ceil = [[0 for i in range(w)] for j in range(h)]
        # 将存活的life置到单元格中
        for pos in self.alive_life:
            self.__set_life(tmp_world_ceil, pos, True)

        self.world_ceil = tmp_world_ceil
        self.width = w
        self.height = h

    def set_origin(self, origin_arr):
        for origin in origin_arr:
            self.add_pos_to_origin(origin)

    def add_pos_to_origin(self, pos):
        WLog.d("add pos (%d,%d)" % (pos[0], pos[1]))
        self.__set_life(self.world_ceil, pos, True)
        self.alive_life.append(pos)

    def reset(self):
        self.iter_cnt = 0
        self.world_ceil = [[0 for i in range(self.width)] for j in range(self.height)]
        self.alive_life.clear()

    def __pos_is_outside(self, pos):
        if pos[0] < 0 or pos[1] < 0 \
                or pos[0] > self.width-1 or pos[1] > self.height - 1:
            return True
        return False

    def __is_alive(self, pos):
        if not self.__pos_is_outside(pos):
            return self.world_ceil[pos[1]][pos[0]] == 1
        return False

    # ceil_list: 需要设置点的来源网格list
    # pos: 设置点位置
    def __set_life(self, ceil_list, pos, alive):
        if self.__pos_is_outside(pos):
            return
        ceil_list[pos[1]][pos[0]] = (1 if alive else 0)

    def __iterate_life(self, pos):
        pos_x = pos[0]
        pos_y = pos[1]
        neighbours = [(pos_x-1, pos_y-1), (pos_x, pos_y-1),
                  (pos_x+1, pos_y-1), (pos_x-1, pos_y),
                  (pos_x+1, pos_y), (pos_x-1, pos_y+1),
                  (pos_x, pos_y+1), (pos_x+1, pos_y+1)]
        neighbours_alive_cnt = 0
        for neighbour in neighbours:
                if self.__is_alive(neighbour):
                    neighbours_alive_cnt += 1

        if self.__is_alive(pos):
            # 少于2个死亡 2/3个的时候才活着
            if neighbours_alive_cnt == 2 or neighbours_alive_cnt == 3:
                self.alive_life.append(pos)
        else:
            # 附近有3个才活着
            if neighbours_alive_cnt == 3:
                self.alive_life.append(pos)

    def iterate(self):
        WLog.d("iterate time: %d " % self.iter_cnt)
        self.iter_cnt += 1
        self.alive_life.clear()
        # 找出本轮迭代存活下来的life
        for j in range(self.height):
            for i in range(self.width):
                pos = [i, j]
                self.__iterate_life(pos)
        # 重置整个世界的单元格
        self.world_ceil = [[0 for i in range(self.width)] for j in range(self.height)]
        # 将存活的life置到单元格中
        for pos in self.alive_life:
            self.__set_life(self.world_ceil, pos, True)

    def run(self, callback):
        for pos in self.alive_life:
            callback(pos, self.__is_alive(pos))