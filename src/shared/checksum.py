from os import readlink, curdir
from os.path import isdir, islink, relpath, exists, isfile, dirname, abspath, join

from shared.hash import encodeBase64, sha1sum

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
        return sha1sum(path)

def readChecksumTXT(filename, sep="  "):
    checksumDict = {}

    if not exists(filename):
        return checksumDict

    with open(filename) as f:
        content = f.read().splitlines()

    for line in content:
        checksum = line.split(sep)[0]
        key = line[len(checksum) + len(sep):]
        checksumDict[key] = checksum

    return checksumDict

def writeChecksumTXT(filename, checksumDict, sep="  "):
    with open(filename, "w") as f:
        for key in checksumDict:
            f.write(f"{checksumDict[key]}{sep}{key}\n")
        f.close()
