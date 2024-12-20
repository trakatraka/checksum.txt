from os import readlink, curdir
from os.path import isdir, islink, relpath, exists, dirname, abspath, join

from shared.hash import encodeBase64, sha1sum, sha256sum
from shared.log import debug
from time import time

DEFAULT_HASH_ALGORITHM = "sha256"

ALGORITHM = DEFAULT_HASH_ALGORITHM

def initHashWithArgs(args):
    if args.hash != None:
        global ALGORITHM
        ALGORITHM = args.hash

def calculateChecksumTXTKeyForPath(path, checksumPath):
    return relpath(abspath(path), dirname(abspath(checksumPath)))

def calculateChecksumTXTPathForKey(key, checksumPath):
    return abspath(join(dirname(checksumPath), key))

def calculateChecksumTXTValueForKey(key, checksumPath):
    path = calculateChecksumTXTPathForKey(key, checksumPath)
    if islink(path):
        return encodeBase64(readlink(path))
    elif isdir(path):
        return encodeBase64(key)
    else:
        if ALGORITHM == "sha1":
            return sha1sum(path)
        elif ALGORITHM == "sha256":
            return sha256sum(path)
        else:
            raise ValueError(f'hash algorithm {ALGORITHM} not supported.')


def readChecksumTXT(filename, sep="  "):
    MS_FROM_START = int(round(time() * 1000))
    debug(f"reading checksum.txt [{filename}]")
    checksumDict = {}

    if not exists(filename):
        return checksumDict

    with open(filename) as f:
        content = f.read().splitlines()

    for line in content:
        checksum = line.split(sep)[0]
        key = line[len(checksum) + len(sep):]
        checksumDict[key] = checksum

    took = int(round(time() * 1000)) - MS_FROM_START
    debug(f"reading checksum.txt [{filename}] took [{took}]")
    return checksumDict

def writeChecksumTXT(filename, checksumDict, sep="  "):
    with open(filename, "w") as f:
        for key in checksumDict:
            f.write(f"{checksumDict[key]}{sep}{key}\n")
        f.close()
