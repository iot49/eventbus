def setSrcAddr(addr: str) -> None:
    """Set the source address for events."""
    global __SRC_ADDR__
    __SRC_ADDR__ = addr


def getSrcAddr() -> str:
    """Get the source address for events."""
    global __SRC_ADDR__
    return __SRC_ADDR__


def eid2eid(eid):
    """Pad if needed. Returns <tree_id>.<branch_id>.<device_id>.<attribute_id>"""
    if eid.count(".") == 1:
        return f"{getSrcAddr()}.{eid}"
    return eid


def eid2did(eid):
    """<tree_id>.<branch_id>.<branch_id>"""
    return ".".join(eid[:3])


def eid2addr(eid):
    """<tree_id>.<branch_id>"""
    return ".".join(eid.split(".")[:2])


# TODO: create srcAddr from config
setSrcAddr("tid.bid")
