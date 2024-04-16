from . import Event


class Ping(Event):
    def __init__(self):
        super().__init__(dst="#ping")


class Pong(Event):
    def __init__(self):
        super().__init__(dst="#pong")


ping = Ping()
pong = Pong()
