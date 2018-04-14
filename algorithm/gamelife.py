# -*- coding:UTF-8 -*-

from utils.logger import WLog

class GameLife:
    def __init__(self, w, h):
        self.width = w
        self.height = h
        self.alive_life = set()
        self.last_alive_life = set()
        self.iter_cnt = 0
        WLog.d("w:%d h:%d" % (w, h))

    def update_size(self, w, h):
        self.width = w
        self.height = h

    def set_origin(self, origin_arr):
        for origin in origin_arr:
            self.add_pos_to_origin(origin)

    def add_pos_to_origin(self, pos):
        pos = tuple(pos)
        WLog.d("add pos (%d,%d)" % (pos[0], pos[1]))
        self.alive_life.add(pos)
        self.last_alive_life.add(pos)

    def reset(self):
        self.iter_cnt = 0
        self.alive_life.clear()
        self.last_alive_life.clear()

    def __is_alive(self, pos):
        if pos in self.last_alive_life:
            return True
        return False

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
                self.alive_life.add(pos)
        else:
            # 附近有3个才活着
            if neighbours_alive_cnt == 3:
                self.alive_life.add(pos)

    def iterate(self):
        WLog.d("iterate time: %d  alive ceil cnt: %d" % (self.iter_cnt, len(self.last_alive_life)))
        self.alive_life.clear()
        # 找出本轮迭代存活下来的life
        for j in range(self.height):
            for i in range(self.width):
                pos = (i, j)
                self.__iterate_life(pos)
        # 将存活的life置到单元格中
        self.last_alive_life.clear()
        for pos in self.alive_life:
            self.last_alive_life.add(pos)

        self.iter_cnt += 1

    def run(self, callback):
        for pos in self.alive_life:
            callback(pos, self.__is_alive(pos))