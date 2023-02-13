from functools import lru_cache
from time import sleep

@lru_cache(maxsize=128)
def delay(secs):
    sleep(secs)
    return secs

print(delay(10), delay(10), delay(10))