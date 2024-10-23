#!/usr/bin/env python3

from os.path import abspath

from shared.diff import checkForMissingAndChangedFiles
from shared.log import log, error, quit
from shared.checksum import readChecksumTXT

def validate(args):
    sourceChecksumPath = abspath(args.checksum)

    sourceChecksum = readChecksumTXT(sourceChecksumPath)

    keysToDelete, keysToAdd, changedKeys, errorKeys = checkForMissingAndChangedFiles(sourceChecksumPath, sourceChecksum, args.PATHS, args.verbose != 0)

    for errorKey in errorKeys:
        log(f"error reading [{errorKey}]")

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
    if len(errorKeys) > 0:
        error(f"[{len(errorKeys)}] files cannot be read!")

    if len(keysToDelete) + len(changedKeys) + len(keysToAdd) + len(keysToDelete) + len(errorKeys) > 0:
        error(f"validation NOT ok")
        quit(1)
    else:
        log(f"validation OK")
        quit(0)
    