import logging
import watchhen

"""
Contains only structure, not real usage
This works not as good as nested.py, but looks maybe nicer tho
(Only one level allowed, below code does not work)
"""

def fails():
    # Should return data but doesn't
    raise ZeroDivisionError("division by zero")

def child():
    try:
        return fails()
    except ZeroDivisionError as e:
        # Either
        raise watchhen.WatchHenFailed(e)
        # Or custom msg
        raise watchhen.WatchHenFailed("That was not supposed to happen! We tried to divide by 0? How?")

def parent():
    try:
        result = child()
        return {} # handle result of child
    except Exception as e:
        raise e

wh = watchhen.WatchHenFunc(parent, "Device Waschmaschiene")
logging.basicConfig(filename='nested_alternative.log', encoding='utf-8', level=logging.INFO)
logging.info("RESTARTED")

wh()
