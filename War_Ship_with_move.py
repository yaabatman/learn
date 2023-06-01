from random import randint, choice


class Ship:

    def __init__(self, length: int, tp=1, x=None, y=None):
        self._x = x
        self._y = y
        self._length = length
        self._tp = tp
        self._is_move = True
        self._cells = [1] * length

    def set_start_coords(self, x, y):
        self._x = x
        self._y = y

    def get_start_coords(self):
        return self._x, self._y

    def move(self, go):
        if self._is_move:
            x, y = self.get_start_coords()
            if self._tp == 1:
                new_x, new_y = x + go, y
            else:
                new_x, new_y = x, y + go

            self.set_start_coords(new_x, new_y)

    def _get_cells_on_pole(self):
        res = []
        l = self._length
        x, y = self.get_start_coords()
        start, stop = 2, l + 1
        if self._tp == 1:
            for i in range(-1, start):
                for j in range(-1, stop):
                    res.append((x + j, y + i))
        else:
            for i in range(-1, start):
                for j in range(-1, stop):
                    res.append((x + i, y + j))
        return res

    def _get_cells_ship(self):
        res = []
        x, y = self.get_start_coords()
        if self._tp == 1:
            for i in range(self._length):
                res.append((x + i, y))
        else:
            for i in range(self._length):
                res.append((x, y + i))

        return res

    def is_collide(self, ship):
        cells = ship._get_cells_ship()
        for t in self._get_cells_on_pole():
            if t in cells:
                return True
        return False

    def is_out_pole(self, size):
        top = self.get_start_coords()
        if self._tp == 1:
            end = (top[0] + self._length - 1, top[1])
        else:
            end = (top[0], top[1] + self._length - 1)

        if not all(0 <= coord < size for coord in top) or not all(0 <= coord < size for coord in end):
            return True
        return False

    def __getitem__(self, item):
        return self._cells[item]

    def __setitem__(self, key, value):
        self._cells[key] = value


class GamePole:
    def __init__(self, size=10):
        self._size = size
        self._ships = []
        self._game_map = tuple([0] * self._size for _ in range(self._size))

    def get_ships(self):
        return self._ships

    def move_ships(self):
        for ship in self._ships:
            if not ship._is_move:
                continue
            old_x, old_y = ship.get_start_coords()
            to = choice((1, -1))
            count = 0
            while count < 2:
                ship.move(to)
                if ship.is_out_pole(self._size) or any(ship.is_collide(s) for s in self._ships if s != ship):
                    to = (1, -1)[to > 0]
                    count += 1
                    ship.set_start_coords(old_x, old_y)
                    continue

    def __check_cells(self, x, y, orient, l):
        start, stop = 2, l + 1
        if orient == 1:
            for i in range(-1, start):
                for j in range(-1, stop):
                    if 0 <= x + j < self._size and 0 <= y + i < self._size:
                        if self._game_map[x + j][y + i]:
                            return False
        else:
            for i in range(-1, start):
                for j in range(-1, stop):
                    if 0 <= x + i < self._size and 0 <= y + j < self._size:
                        if self._game_map[x + i][y + j]:
                            return False
        return True

    def init(self):
        self._ships = [Ship(1, tp=randint(1, 2)), Ship(1, tp=randint(1, 2)),
                       Ship(1, tp=randint(1, 2)), Ship(1, tp=randint(1, 2)),
                       Ship(2, tp=randint(1, 2)), Ship(2, tp=randint(1, 2)),
                       Ship(2, tp=randint(1, 2)), Ship(3, tp=randint(1, 2)),
                       Ship(3, tp=randint(1, 2)), Ship(4, tp=randint(1, 2))]
        n = self._size - 1
        for ship in self._ships[::-1]:
            while True:
                x, y = randint(0, n), randint(0, n)
                len_ship = ship._length
                orient = ship._tp
                if self._game_map[x][y]:
                    continue
                if not self.__check_cells(x, y, orient, len_ship):
                    continue
                ship.set_start_coords(x, y)
                if ship.is_out_pole(self._size):
                    continue
                if orient == 1:
                    for i in range(len_ship):
                        self._game_map[x + i][y] = ship
                if orient == 2:
                    for i in range(len_ship):
                        self._game_map[x][y + i] = ship
                break

    def show(self):
        for row in self._game_map:
            print(*(1 if isinstance(i, Ship) else i for i in row))

    def get_pole(self):
        return tuple(tuple(row) for row in self._game_map)
