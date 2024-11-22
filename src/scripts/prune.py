from os.path import abspath

from shared.checksum import readChecksumTXT, writeChecksumTXT
from shared.diff import checkForMissingFilesInChecksum
from shared.log import log, quit, debug
from time import time

def prune(args):
    sourceChecksumPath = abspath(args.checksum)

    sourceChecksum = readChecksumTXT(sourceChecksumPath)

    missingKeys = checkForMissingFilesInChecksum(sourceChecksumPath, sourceChecksum)

    MS_FROM_START = int(round(time() * 1000))
    log(f"removing {len(missingKeys)} missing files from checksum.txt")

    for key in missingKeys:
        debug(f'{key} removing from checksum.txt!')
        del(sourceChecksum[key])

    took = int(round(time() * 1000)) - MS_FROM_START
    log(f"removing {len(missingKeys)} missing files from checksum.txt took {took}ms")

    for key in missingKeys:
        log(f"[{key}] missing")

    log(f"[{len(missingKeys)}] missing files removed")

    if args.dry_run == 0:
        log(f"writing changes to checksum.txt")
        writeChecksumTXT(sourceChecksumPath, sourceChecksum)
        quit(0)
    else:
        log(f"not writing changes to checksum.txt")
        quit(0)
