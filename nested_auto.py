import logging
import watchhen

"""
Contains only structure, not real usage
Does not work currently, requires some work
"""

@watchhen.nested
def fails():
    # Should return data but doesn't
    raise ZeroDivisionError("division by zero")

@watchhen.nested
def child():
    try:
        return fails()
    except ZeroDivisionError as e:
        # Either
        return watchhen.WatchHenFailed(e)
        # Or custom msg
        return watchhen.WatchHenFailed("That was not supposed to happen! We tried to divide by 0? How?")


def parent():
    result = child()
    return {} # handle result of child

wh = watchhen.WatchHenFunc(parent, "Device Waschmaschiene")
logging.basicConfig(filename='nested_auto.log', encoding='utf-8', level=logging.INFO)
logging.info("RESTARTED")

wh()
