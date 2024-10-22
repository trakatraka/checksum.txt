from base64 import b64encode
from hashlib import sha1

def sha1sum(filename):
    h  = sha1()
    b  = bytearray(128*1024)
    mv = memoryview(b)
    with open(filename, 'rb', buffering=0) as f:
        while n := f.readinto(mv):
            h.update(mv[:n])
    return h.hexdigest()

def encodeBase64(str):
    return b64encode(str.encode("utf-8")).decode("utf-8")