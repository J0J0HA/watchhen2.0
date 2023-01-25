import logging
import watchhen

"""
Contains only structure, not real usage
"""

def fails():
    # Should return data but doesn't
    raise ZeroDivisionError("division by zero")

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
    if not watchhen.failed(result):
        return {} # handle result of child
    return result

wh = watchhen.WatchHenFunc(parent, "Device Waschmaschiene")
logging.basicConfig(filename='nested.log', encoding='utf-8', level=logging.INFO)
logging.info("RESTARTED")

wh()
