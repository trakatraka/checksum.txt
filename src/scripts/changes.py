#!/usr/bin/env python3

from os.path import abspath

from shared.diff import checkChanges
from shared.log import log, quit, error
from shared.checksum import readChecksumTXT

def changes(args):
    sourceChecksumPath = abspath(args.checksum)

    sourceChecksum = readChecksumTXT(sourceChecksumPath)

    keysToDelete, keysToAdd, changedKeys, errorKeys = checkChanges(sourceChecksumPath, sourceChecksum, args)

    for errorKey in errorKeys:
        log(f"error reading [{errorKey}]")

    log(f"[{len(keysToDelete)}] missing  files")
    log(f"[{len(keysToAdd)}] files added")
    log(f"[{len(changedKeys)}] files changed")
    if len(errorKeys) > 0:
        error(f"[{len(errorKeys)}] files cannot be read!")

    if len(keysToDelete) + len(changedKeys) + len(keysToAdd) + len(errorKeys) > 0:
        quit(1)
    else:
        quit(0)

