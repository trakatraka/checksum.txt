from base64 import b64encode
from hashlib import sha1
from shared.log import debug
from time import time

def sha1sum(filename):
    MS_FROM_START = int(round(time() * 1000))
    debug(f"calculating sha1 for [{filename}]")
    h  = sha1()
    b  = bytearray(128*1024)
    mv = memoryview(b)
    with open(filename, 'rb', buffering=0) as f:
        while n := f.readinto(mv):
            h.update(mv[:n])
    digest=h.hexdigest()
    took = int(round(time() * 1000)) - MS_FROM_START
    debug(f"calculating sha1 for [{filename}] took {took}ms")
    return digest

def encodeBase64(str):
    return b64encode(str.encode("utf-8")).decode("utf-8")