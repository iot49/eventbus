import time

from . import event_type
from .eid import eid2addr, eid2did, eid2eid, getSrcAddr

Event = dict

# MicroPython time starts from 2000-01-01 on some ports
EPOCH_OFFSET = 946684800 if time.gmtime(0)[0] == 2000 else 0


ping = {"et": event_type.PING, "src": getSrcAddr()}
pong = {"et": event_type.PONG, "src": getSrcAddr()}

get_state = {"et": event_type.GET_STATE, "dst": "#server", "src": getSrcAddr()}
get_config = {"et": event_type.GET_CONFIG, "dst": "#server", "src": getSrcAddr()}
get_log = {"et": event_type.GET_LOG, "dst": "#server", "src": getSrcAddr()}

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
