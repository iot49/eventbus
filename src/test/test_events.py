import time
from datetime import datetime, timezone

import eventbus
from eventbus.event import Hello, State, ping, pong

eventbus.SRC_ADDR = "tree.branch"  # noqa: F811


def is_subset(first, second):
    sentinel = object()
    return all(first[key] == second.get(key, sentinel) for key in first)


def test_events():
    assert ping.to_dict() == {"model": "Ping", "src": eventbus.SRC_ADDR, "dst": "#ping"}
    assert pong.to_dict() == {"model": "Pong", "src": eventbus.SRC_ADDR, "dst": "#pong"}
    proto = {
        "model": "Hello",
        "success": "Connected",
        "src": eventbus.SRC_ADDR,
        "dst": "@client5",
    }
    assert Hello(success=proto["success"], dst=proto["dst"]).to_dict() == proto
    proto = {
        "model": "Hello",
        "error": "Timeout",
        "src": eventbus.SRC_ADDR,
        "dst": "@client5",
    }
    assert Hello(error=proto["error"], dst=proto["dst"]).to_dict() == proto


def test_state():
    ENTITY = "a.b"
    VALUE = 1.23
    DT = 0.01

    state = State(entity_id=ENTITY, value=VALUE)
    proto = {
        "model": "State",
        "entity_id": f"{eventbus.SRC_ADDR}.{ENTITY}",
        "value": VALUE,
        "src": eventbus.SRC_ADDR,
    }
    ts1 = state.timestamp
    assert is_subset(proto, state.to_dict())
    time.sleep(DT)
    state.value = VALUE + 1
    proto["value"] = VALUE + 1
    ts2 = state.timestamp
    assert ts2 >= ts1 + DT
    assert is_subset(proto, state.to_dict())

    dt = datetime.fromtimestamp(time.time(), timezone.utc)
    assert str(state.datetime())[:19] == str(dt)[:19]
    assert state.updated_at()[:19] == str(dt)[:19]
