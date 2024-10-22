#!/usr/bin/env python3

from os.path import abspath

from shared.diff import checkForMissingAndChangedFiles
from shared.log import log, error, quit

def validate(args):
    sourceChecksumPath = abspath(args.checksum)

    keysToDelete, keysToAdd, changedKeys = checkForMissingAndChangedFiles(sourceChecksumPath, args.PATHS, args.verbose != 0)

    if len(keysToDelete) > 0:
        error(f"[{len(keysToDelete)}] missing  files")
    else:
        log(f"[{len(keysToDelete)}] missing  files")
    if len(keysToAdd) > 0:
        error(f"[{len(keysToAdd)}] files added")
    else:
        log(f"[{len(keysToAdd)}] files added")
    if len(changedKeys) > 0:
        error(f"[{len(changedKeys)}] files changed")
    else:
        log(f"[{len(changedKeys)}] files changed")

    if len(keysToDelete) + len(changedKeys) + len(keysToAdd) + len(keysToDelete) > 0:
        error(f"validation NOT ok")
        quit(1)
    else:
        log(f"validation OK")
        quit(0)
    