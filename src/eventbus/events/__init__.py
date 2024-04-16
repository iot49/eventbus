# ruff: noqa: F401, E402

from io import StringIO
from typing import Optional

from pydantic import BaseModel

"""
Branch address of the processor this module is running on.
Used to initialize Event.src.

IMPORTANT: Set this before creating any Event instances!
"""


class Event(BaseModel):
    # addressing
    src: Optional[str] = None
    dst: str

    def to_dict(self) -> dict:
        from .. import SRC_ADDR

        assert SRC_ADDR is not None, "SRC_ADDR is not set!"
        d = self.model_dump(exclude_none=True, exclude_defaults=True, exclude_unset=True)
        d["model"] = self.__class__.__name__
        d["src"] = SRC_ADDR
        return d

    @classmethod
    def from_dict(cls, data: dict) -> "Event":
        assert isinstance(data, dict)
        model = globals()[data["model"]]
        return model(**data)


from .hello import Hello
from .ping_pong import ping, pong
from .state import GetState, State, StateAction
