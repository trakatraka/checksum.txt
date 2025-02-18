from os.path import abspath

from os.path import dirname
from shared.checksum import readChecksumTXT, calculateChecksumTXTValueForKey, writeChecksumTXT
from shared.diff import checkForFilesNotInChecksum
from shared.log import log, quit, logProgress
from time import time

def append(args):
    sourceChecksumPath = abspath(args.checksum)

    sourceChecksum = readChecksumTXT(sourceChecksumPath)

    keysToAdd = checkForFilesNotInChecksum(sourceChecksumPath, sourceChecksum, args.PATHS)

    MS_FROM_START = int(round(time() * 1000))
    log(f"calculating {len(keysToAdd)} checksums")
    runned=0
    for key in keysToAdd:
        try:
            value = calculateChecksumTXTValueForKey(key, sourceChecksumPath)
            sourceChecksum[key] = value
            runned+=1
            logProgress(dirname(key), runned, len(keysToAdd))
        except Exception as e:
            error(e)
            error(f"error calculating for {key}")
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
