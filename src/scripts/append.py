from os.path import abspath

from shared.checksum import readChecksumTXT, calculateChecksumTXTValueForKey, writeChecksumTXT
from shared.diff import checkForFilesNotInChecksum
from shared.log import log, quit
from time import time

def append(args):
    sourceChecksumPath = abspath(args.checksum)

    sourceChecksum = readChecksumTXT(sourceChecksumPath)

    keysToAdd = checkForFilesNotInChecksum(sourceChecksumPath, sourceChecksum, args.PATHS)

    MS_FROM_START = int(round(time() * 1000))
    log(f"calculating {len(keysToAdd)} checksums")

    for key in keysToAdd:
        value = calculateChecksumTXTValueForKey(key, sourceChecksumPath)
        sourceChecksum[key] = value
    took = int(round(time() * 1000)) - MS_FROM_START
    log(f"calculating {len(keysToAdd)} checksums took {took}ms")

    for key in keysToAdd:
        log(f"[{key}] added")

    log(f"[{len(keysToAdd)}] files added")

    if args.dry_run == 0:
        log(f"writing changes to checksum.txt")
        writeChecksumTXT(sourceChecksumPath, sourceChecksum)
        quit(0)
    else:
        log(f"not writing changes to checksum.txt")
        quit(0)
