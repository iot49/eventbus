import time

from . import event_type
from .eid import eid2addr, eid2did, eid2eid, getSrcAddr

"""
Events are dicts communicated by EventBus.

The following fields are mandatory:

- et: event type (and int defined in event_type.py)
- src: source address (str)
- dst: destination address (str)

All other fields are specific to the event type. To keep
things organized, events should not be created ad-hoc.
This file defines a set of functions to create events for
an application. For other purposes, it should be modified
or extended.
"""

# MicroPython time starts from 2000-01-01 on some ports
EPOCH_OFFSET = 946684800 if time.gmtime(0)[0] == 2000 else 0

# connection keep-alive
ping = {"et": event_type.PING, "src": getSrcAddr()}
pong = {"et": event_type.PONG, "src": getSrcAddr()}

# states
get_state = {"et": event_type.GET_STATE, "dst": "#server", "src": getSrcAddr()}
get_config = {"et": event_type.GET_CONFIG, "dst": "#server", "src": getSrcAddr()}
get_log = {"et": event_type.GET_LOG, "dst": "#server", "src": getSrcAddr()}

# connection management
hello_connected = {"et": event_type.HELLO_CONNECTED, "src": getSrcAddr()}
hello_no_token = {"et": event_type.HELLO_NO_TOKEN, "src": getSrcAddr()}
hello_invalid_token = {"et": event_type.HELLO_INVALID_TOKEN, "src": getSrcAddr()}

bye = {"et": event_type.BYE, "src": getSrcAddr()}
bye_timeout = {"et": event_type.BYE_TIMEOUT, "src": getSrcAddr()}


def state(eid: str, value, dst="#clients", timestamp: float = time.time() + EPOCH_OFFSET):
    return {
        "et": event_type.STATE,
        "eid": eid2eid(eid),
        "value": value,
        "timestamp": timestamp,
        "src": getSrcAddr(),
        "dst": dst,
    }


def state_update(state: dict, value):
    state["value"] = value
    state["timestamp"] = time.time() + EPOCH_OFFSET
    return state


def state_action(state: dict, action: str, param=None):
    eid = state["eid"]
    return {
        "et": event_type.STATE_ACTION,
        "device_id": eid2did(eid),
        "action": action,
        "param": param,
        "src": getSrcAddr(),
        "dst": eid2addr(eid),
    }
