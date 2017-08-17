from functools import wraps


def has_traitsui():
    """ Is traitsui installed? """
    try:
        import traitsui
    except ImportError:
        return False
    return True


def skip_if_no_traitsui(test):
    """ Decorator that skips test if traitsui not available """
    @wraps(test)
    def new_test(self):
        if has_traitsui():
            test(self)
        else:
            self.skipTest("Can't import traitsui.")
    return new_test
