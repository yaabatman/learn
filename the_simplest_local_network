'''Нужно реализовать простую имитацию локальной сети, состоящую из набора серверов,
 соединенных между собой через роутер. Каждый сервер может отправлять пакет любому другому серверу сети.
  Для этого у каждого есть свой уникальный IP-адрес.
  Для простоты - это просто целое (натуральное) число от 1 и до N,
   где N - общее число серверов. Алгоритм следующий.
    Предположим, сервер с IP = 2 собирается отправить пакет информации серверу с IP = 3.
     Для этого, он сначала отправляет пакет роутеру, а уже тот,
      смотрит на IP-адрес и пересылает пакет нужному узлу (серверу).'''


class Server:
    __IP = 0

    def __init__(self):
        Server.__IP += 1
        self.ip = Server.__IP
        self.buffer = []
        self.router = None

    def send_data(self, data):
        if self.router:
            self.router.buffer.append(data)

    def get_data(self):
        res = self.buffer.copy()
        self.buffer.clear()
        return res

    def get_ip(self):
        return self.ip


class Router:

    def __init__(self):
        self.buffer = []
        self.servers = {}

    def link(self, server):
        self.servers[server.ip] = server
        server.router = self

    def unlink(self, server):
        key = server.ip
        if key in self.servers:
            self.servers.pop(key)
            server.router = None

    def send_data(self):
        for d in self.buffer:
            if d.ip in self.servers:
                self.servers[d.ip].buffer.append(d)
        self.buffer.clear()


class Data:

    def __init__(self, data, ip):
        self.data = data
        self.ip = ip
