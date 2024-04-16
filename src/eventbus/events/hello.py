from . import Event


class Hello(Event):
    success: str | None = None
    error: str | None = None
