import time

from . import event_type

Event = dict

SRC_ADDR = "tree.branch"

# MicroPython time starts from 2000-01-01 on some ports
EPOCH_OFFSET = 946684800 if time.gmtime(0)[0] == 2000 else 0


ping = {"et": event_type.PING}
pong = {"et": event_type.PONG}

get_state = {"et": event_type.GET_STATE, "dst": "#server"}
get_config = {"et": event_type.GET_CONFIG, "dst": "#server"}
get_log = {"et": event_type.GET_LOG, "dst": "#server"}


def state(entity_id: str, value, dst="#clients", timestamp: float = time.time() + EPOCH_OFFSET):
    if entity_id.count(".") == 1:
        entity_id = f"{SRC_ADDR}.{entity_id}"
    return {
        "et": event_type.STATE,
        "entity_id": entity_id,
        "value": value,
        "timestamp": timestamp,
        "dst": dst,
    }


def state_update(state: dict, value):
    state["value"] = value
    state["timestamp"] = time.time() + EPOCH_OFFSET
    return state


def state_action(state: dict, action: str, param=None):
    eid = state["entity_id"].split(".")
    device_id = ".".join(eid[:3])
    dst = ".".join(eid[:2])
    return {
        "et": event_type.STATE_ACTION,
        "device_id": device_id,
        "action": action,
        "param": param,
        "dst": dst,
    }


def hello(success: str = None, error: str = None):  # type: ignore
    res: dict = {"et": event_type.HELLO}
    if success is not None:
        res["success"] = success
    if error is not None:
        res["error"] = error
    return res
