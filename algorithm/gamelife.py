# -*- coding:UTF-8 -*-

from utils.logger import WLog

class GameLife:
    def __init__(self, w, h, max_w, max_h):
        self.max_w = max_w
        self.max_h = max_h
        self.width = w
        self.height = h
        self.alive_life = set()
        self.last_alive_life = set()
        self.iter_cnt = 0
        WLog.d("w:%d h:%d" % (w, h))

    def update_size(self, w, h, max_w, max_h):
        self.width = w
        self.height = h
        self.max_w = max_w
        self.max_h = max_h

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
        neighbours = self.__get_neighbourd(pos)
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

    def __get_neighbourd(self, pos):
        pos_x = pos[0]
        pos_y = pos[1]
        return ((pos_x-1, pos_y-1), (pos_x, pos_y-1),
                  (pos_x+1, pos_y-1), (pos_x-1, pos_y),
                  (pos_x+1, pos_y), (pos_x-1, pos_y+1),
                  (pos_x, pos_y+1), (pos_x+1, pos_y+1))

    def __is_out_limit(self, pos):
        return pos[0] < 0 or pos[1] < 0 or pos[0] > self.max_w or pos[1] > self.max_h

    def iterate(self):
        WLog.d("iterate time: %d  alive ceil cnt: %d" % (self.iter_cnt, len(self.last_alive_life)))
        self.alive_life = set()

        iterate_set = set()
        for pos in self.last_alive_life:
            neighbours = self.__get_neighbourd(pos)
            for neighbour in neighbours:
                if not self.__is_out_limit(neighbour):
                    iterate_set.add(neighbour)
        for pos in iterate_set:
            self.__iterate_life(pos)

        # 将存活的life置到单元格中
        self.last_alive_life = self.alive_life
        self.iter_cnt += 1

    def run(self, callback):
        for pos in self.last_alive_life:
            callback(pos, True)