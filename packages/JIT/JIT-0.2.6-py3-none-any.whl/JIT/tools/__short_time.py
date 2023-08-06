import time


def delayMicrosecond(t):
    """
    this func running better in linux ,for windows at least 1000 us
    :param t: us
    :return:
    """
    start, end = 0, 0
    start = time.time()
    t = (t - 1) / 1000000
    while end - start < t:
        end = time.time()


