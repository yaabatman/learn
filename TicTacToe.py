from random import randint


class Cell:
    def __init__(self):
        self.value = 0    # 0-свободдно, 1-крестик, 2-нолик

    def __bool__(self):
        return self.value == 0


class TicTacToe:
    FREE_CELL = 0  # свободная клетка
    HUMAN_X = 1  # крестик (игрок - человек)
    COMPUTER_O = 2  # нолик (игрок - компьютер)

    def __init__(self):
        self.__n = 3
        self._win = 0    # 0 - game, 1 - wim human, 2 - win PC, 3 - draw
        self.pole = tuple(tuple(Cell() for _ in range(self.__n)) for _ in range(self.__n))

    def __check_index(self, index):
        if not all(isinstance(x, int) for x in index) or\
                not (0 <= index[0] < self.__n or 0 <= index[1] < self.__n):
            raise IndexError('некорректно указанные индексы')

    def __update_win_status(self):
        for row in self.pole:
            if all(x.value == self.HUMAN_X for x in row):
                self._win = 1
                return
            if all(x.value == self.COMPUTER_O for x in row):
                self._win = 2
                return

        for i in range(self.__n):
            if all(x.value == self.HUMAN_X for x in (row[i] for row in self.pole)):
                self._win = 1
                return
            if all(x.value == self.COMPUTER_O for x in (row[i] for row in self.pole)):
                self._win = 2
                return

        if all(self.pole[i][i].value == self.HUMAN_X for i in range(self.__n)) or \
            all(self.pole[i][-1 - i].value == self.HUMAN_X for i in range(self.__n)):
            self._win = 1
            return

        if all(self.pole[i][i].value == self.COMPUTER_O for i in range(self.__n)) or \
            all(self.pole[i][-1 - i].value == self.COMPUTER_O for i in range(self.__n)):
            self._win = 2
            return

        if all(x.value != self.FREE_CELL for row in self.pole for x in row):
            self._win = 3

    def __getitem__(self, item):
        self.__check_index(item)
        return self.pole[item[0]][item[1]].value

    def __setitem__(self, key, value):
        self.__check_index(key)
        self.pole[key[0]][key[1]].value = value
        self.__update_win_status()

    def init(self):
        for line in self.pole:
            for cell in line:
                cell.value = 0
        self._win = 0

    def show(self):
        for line in self.pole:
            print(*map(lambda x: '#' if x.value == self.FREE_CELL else x.value, line))
        print()

    def human_go(self):
        if not self:
            return

        while True:
            i, j = map(int, input('введите координаты клетки через пробел от 0 до 2\n').split())
            if not (0 <= i < self.__n) or not (0 <= j < self.__n):
                continue
            if self[i, j] == self.FREE_CELL:
                self[i, j] = self.HUMAN_X
                break

    def computer_go(self):
        if not self:
            return

        while True:
            i = randint(0, self.__n - 1)
            j = randint(0, self.__n - 1)
            if self[i, j] != self.FREE_CELL:
                continue
            self[i, j] = self.COMPUTER_O
            break

    @property
    def is_human_win(self):
        return self._win == 1

    @property
    def is_computer_win(self):
        return self._win == 2

    @property
    def is_draw(self):
        return self._win == 3

    def __bool__(self):
        return self._win == 0 and self._win not in (1, 2, 3)
