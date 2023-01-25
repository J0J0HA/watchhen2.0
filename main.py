import logging
import watchhen


def test(a):
    match a:
        case 0:
            return
        case 1:
            raise TypeError(a)
        case 2:
            raise ValueError(a)
        case 3:
            return watchhen.WatchHenFailed("This is a test")

logging.basicConfig(filename='main.log', encoding='utf-8', level=logging.INFO)
logging.info("RESTARTED")
wh = watchhen.WatchHenFunc(test, "Device Waschmaschiene")

# Causing some errors
wh(0)
wh(1)
wh(1)
wh(1)
wh(1)
wh(1)
wh(1)
wh(2)
wh(2)
wh(2)
wh(3)
wh(0)


# An additional way to create watchhens, not required for you
@watchhen.watchhen("Test")
def t2():
    pass

@watchhen.watchhen
def t3():
    pass
