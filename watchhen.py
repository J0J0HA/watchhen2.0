import logging
import typing



MESSAGES = {
    "new_reason": "{name} now fails with error {new_err} after failing {off_since} times with error {old_err}",
    "succeeded": "{name} succeeded",
    "failed": "{name} failed with error {err}",
    "is_offline": "{name} failed with error {err}",
    "went_offline": "{name} failed with error {err} multiple times and was marked as offline",
    "went_online": "{name} succeeded again after {off_since} fails and was marked as online"
}

def nested_mapped(map: dict):
    def wrapper(func: typing.Callable):
        def decorator(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                if failed(result):
                    return result
                return result
            except Exception as e:
                if type(e) in map:
                    return WatchHenFailed(map[type(e)])
                return WatchHenFailed(e)
        return decorator
    return wrapper


def nested(func: typing.Callable):
    def decorator(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            return WatchHenFailed(e)
    return decorator

def failed(obj: object):
    return isinstance(obj, WatchHenFailed)

def watchhen(name_or_func: typing.Union[str, typing.Callable] = "Unnamed WatchHen", logger: logging.Logger = logging, messages = MESSAGES):
    def decorator(func: typing.Callable, name: str = name_or_func):
        return WatchHenFunc(func, name_or_func, logger, messages)
    if isinstance(name_or_func, str):
        return decorator
    else:
        return decorator(name_or_func, "Unnamed WatchHen")


class WatchHenFailed(BaseException): pass

class WatchHenFunc:
    def __init__(self, func: typing.Callable, name: str = "Unnamed WatchHen", logger: logging.Logger = logging, messages: dict = MESSAGES):
        # Static Values
        self.name = name
        self.func = func
        self.logger = logger

        # Static Messages
        self.new_reason_msg = messages["new_reason"]
        self.succeeded_msg = messages["succeeded"]
        self.failed_msg = messages["failed"]
        self.is_offline_msg = messages["is_offline"]
        self.went_offline_msg = messages["went_offline"]
        self.went_online_msg = messages["went_online"]

        # Variabled used to calculate messages
        self.last_error = None
        self.off_since = 0

    def handle_success(self):
        self.logger.debug(self.succeeded_msg.format(name=self.name))
        # If this was marked as offline
        if self.off_since >= 2:
            self.logger.info(self.went_online_msg.format(name=self.name, err=str(self.last_error), off_since=self.off_since))
        # Reset error count
        self.off_since = 0

    def handle_exception(self, err: Exception):
        self.logger.debug(self.failed_msg.format(name=self.name, err=str(err)))
        # If getting error while not marked as offline
        if self.off_since == 0:
            self.logger.warning(self.is_offline_msg.format(name=self.name, err=str(err)))
        # If getting same error
        elif type(self.last_error) == type(err):
            # If getting it for the first time
            if self.off_since == 1:
                self.logger.error(self.went_offline_msg.format(name=self.name, err=str(err)))
        # If getting different error -> If error changed
        else: # Obmitted "self.off_since >= 2" because it's redundant
            self.logger.info(self.new_reason_msg.format(name=self.name, new_err=str(err), old_err=str(self.last_error), off_since=self.off_since))
        # Increment error count
        self.off_since += 1
        # Set last_error
        self.last_error = err

    def __call__(self, *args, **kwargs):
        try:
            result = self.func(*args, **kwargs)
            # If the function returns a WatchHenFailed(err), the error is processed
            if isinstance(result, WatchHenFailed):
                self.handle_exception(result)
            else:
                self.handle_success()
            return result
        except Exception as err:
            self.handle_exception(err)
            return WatchHenFailed(err)