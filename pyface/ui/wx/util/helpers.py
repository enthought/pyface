from threading import Timer, Event


def wait_until(condition, timeout, *args, **kwargs):
    """ Wait until ``condition`` returns true or timeout elapses.

    Parameters
    ----------
    condition : callable
        A callable checking the desired ``condition`` and returns
        True or False.
    timeout : float
        The timeout, in seconds, to wait for the ``condition`` to return True
    *args :
        Arguments to pass to the ``condition`` callable
    *kwargs :
        Arguments to pass to the ``condition`` callable

    """
    check_now = Event()

    def check_timer():
        timer = Timer(0.5, check_now.set)
        timer.start()

    heartbeats = timeout / 0.5
    while heartbeats >= 1:
        check_now.clear()
        check_timer()
        check_now.wait(timeout)
        if condition(*args, **kwargs):
            break
        else:
            heartbeats -= 1

    if heartbeats == 0:
        raise RuntimeError('Timed out waiting for condition')
