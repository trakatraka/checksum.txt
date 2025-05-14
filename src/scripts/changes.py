#!/usr/bin/env python3

from os.path import abspath

from shared.diff import checkChanges
from shared.log import log, quit, error
from shared.checksum import readChecksumTXT

def changes(args):
    sourceChecksumPath = abspath(args.checksum)

    sourceChecksum = readChecksumTXT(sourceChecksumPath)

    keysToDelete, keysToAdd, changedKeys, errorKeys = checkChanges(sourceChecksumPath, sourceChecksum, args)

    for key in keysToDelete:
        log(f"[{key}] deleted")

    for key in keysToAdd:
        log(f"[{key}] added")

    for key in changedKeys:
        log(f"[{key}] changed")

    for errorKey in errorKeys:
        error(f"error reading [{errorKey}]")

    log(f"[{len(keysToDelete)}] files deleted")
    log(f"[{len(keysToAdd)}] files added")
    log(f"[{len(changedKeys)}] files changed")
    if len(errorKeys) > 0:
        error(f"[{len(errorKeys)}] files cannot be read!")

    total_changes = len(keysToDelete) + len(changedKeys) + len(keysToAdd)
    log(f"total [{total_changes}] changes")
    
    if len(keysToDelete) + len(changedKeys) + len(keysToAdd) + len(errorKeys) > 0:
        quit(1)
    else:
        quit(0)

