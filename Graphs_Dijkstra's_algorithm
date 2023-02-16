'''Необходимо написать универсальную основу для представления ненаправленных связных графов и поиска в них кратчайших маршрутов.
 Далее, этот алгоритм предполагается применять для прокладки маршрутов: на картах, в метро и так далее.'''


import math


class LinkedGraph:
    def __init__(self):
        self._links = []
        self._vertex = []

    def add_vertex(self, v):
        if v not in self._vertex:
            self._vertex.append(v)

    def __find_path(self, x, y):
        return tuple(filter(lambda line: x in line.get_coords() and y in line.get_coords(), self._links))

    def add_link(self, link):
        x, y = link.v1, link.v2
        res = self.__find_path(x, y)
        if not res:
            self._links.append(link)
            self.add_vertex(x)
            self.add_vertex(y)
            x.links.append(link)
            y.links.append(link)

    def __create_matrix(self, n):
        matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                paths = self._vertex[i].links
                res = tuple(filter(lambda obj: self._vertex[j] in obj.get_coords(), paths))
                if res:
                    matrix[i][j] = res[0].dist
        return matrix

    def __get_link(self, start, matrix):
        for i, weight in enumerate(matrix[start]):
            if weight > 0:
                yield i

    def __arg_min(self, infs, vertexes_open):
        min_a = -1
        max_a = max(infs)
        for i, t in enumerate(infs):
            if t < max_a and i not in vertexes_open:
                max_a = t
                min_a = i
        return min_a

    def __algoritm_find_path(self, start_v, matrix, n, stop):
        infs = [math.inf] * n
        start = self._vertex.index(start_v)
        vertexes_open = {start}
        infs[start] = 0
        min_path = [[self._vertex[start]] for _ in range(n)]
        lenght = [[] for _ in range(n)]
        while start != -1:
            for j in self.__get_link(start, matrix):
                if j not in vertexes_open:
                    path = min_path[start] + [self._vertex[j]]
                    leng = lenght[start] + [*self.__find_path(self._vertex[start], self._vertex[j])]
                    weight = infs[start] + matrix[start][j]
                    if weight < infs[j]:
                        infs[j] = weight
                        min_path[j] = path
                        lenght[j] = leng

            start = self.__arg_min(infs, vertexes_open)
            if start > 0:
                vertexes_open.add(start)
        return min_path[stop], lenght[stop],

    def find_path(self, start_v, stop_v):
        n = len(self._vertex)
        matrix = self.__create_matrix(n)
        stop = self._vertex.index(stop_v)
        res = self.__algoritm_find_path(start_v, matrix, n, stop)
        return res


class Vertex:
    def __init__(self):
        self._links = []

    @property
    def links(self):
        return self._links


class Link:
    def __init__(self, v1, v2):
        self._v1 = v1
        self._v2 = v2
        self._dist = 1

    def get_coords(self):
        return self.v1, self.v2

    @property
    def v1(self):
        return self._v1

    @property
    def v2(self):
        return self._v2

    @property
    def dist(self):
        return self._dist

    @dist.setter
    def dist(self, value):
        self._dist = value


class Station(Vertex):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class LinkMetro(Link):
    def __init__(self, v1, v2, dist):
        super().__init__(v1, v2)
        self.dist = dist
