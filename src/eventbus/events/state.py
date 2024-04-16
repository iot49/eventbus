import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Union

from . import Event

# MicroPython time starts from 2000-01-01 on some ports
EPOCH_OFFSET = 946684800 if time.gmtime(0)[0] == 2000 else 0

JSON = Union[Dict[str, Any], List[Any], int, str, float, bool, None]

# <tree_id>.<branch_id>.<device_id>.<attribute_id>
EntityID = str


class GetState(Event):
    def __init__(self):
        super().__init__(dst="#server")


class StateAction(Event):
    kind: str
    entity_id: EntityID
    param: JSON

    def __init__(self, state: "State", kind: str, param: Optional[JSON] = None) -> None:
        super().__init__(
            kind=kind,  # type: ignore
            entity_id=state.entity_id,  # type: ignore
            param=param,  # type: ignore
            dst=".".join(state.entity_id.split(".")[:2]),  # type: ignore
        )


class State(Event):
    entity_id: EntityID
    value: JSON
    timestamp: float

    def __init__(self, entity_id: EntityID, value: JSON) -> None:
        if entity_id.count(".") == 1:
            from .. import SRC_ADDR

            entity_id = f"{SRC_ADDR}.{entity_id}"
        assert entity_id.count(".") == 3, "Entity must have 3 dots"
        super().__init__(dst="#clients", entity_id=entity_id, value=value, timestamp=time.time() + EPOCH_OFFSET)  # type: ignore

    def action(self, kind: str, param: Optional[JSON] = None) -> StateAction:
        """Create an action for this state.

        Examples:
           state.action("turn_on")
           state.action("set_level", level=50)
        """
        return StateAction(state=self, kind=kind, param=param)

    def datetime(self) -> datetime:
        """Return the timestamp as a datetime object."""
        return datetime.fromtimestamp(self.timestamp - EPOCH_OFFSET, timezone.utc)

    def updated_at(self) -> str:
        """Return the timestamp in human readable format."""
        return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(self.timestamp - EPOCH_OFFSET))

    def __setattr__(self, name: str, value: Any) -> None:
        """Update timestamp when value changes."""
        if name == "value":
            self.timestamp = time.time() + EPOCH_OFFSET
        super().__setattr__(name, value)
