#!/usr/bin/env python3

from os.path import abspath

from shared.diff import checkForMissingAndChangedFiles
from shared.log import log, error, quit
from shared.checksum import readChecksumTXT

def validate(args):
    sourceChecksumPath = abspath(args.checksum)

    sourceChecksum = readChecksumTXT(sourceChecksumPath)

    keysToDelete, keysToAdd, changedKeys, errorKeys = checkForMissingAndChangedFiles(sourceChecksumPath, sourceChecksum, args.PATHS)

    for key in keysToDelete:
        log(f"[{key}] deleted")

    for key in keysToAdd:
        log(f"[{key}] added")

    for key in changedKeys:
        log(f"[{key}] changed")

    for errorKey in errorKeys:
        error(f"error reading [{errorKey}]")

    if len(keysToDelete) > 0:
        error(f"[{len(keysToDelete)}] files deleted")
    else:
        log(f"[{len(keysToDelete)}] files deleted")
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
    total_changes = len(keysToDelete) + len(changedKeys) + len(keysToAdd) + len(keysToDelete)
    
    if total_changes > 0:
        error(f"total [{total_changes}] changes")
    else:
        log(f"total [{total_changes}] changes")

    if len(keysToDelete) + len(changedKeys) + len(keysToAdd) + len(keysToDelete) + len(errorKeys) > 0:
        error(f"validation NOT ok")
        quit(1)
    else:
        log(f"validation OK")
        quit(0)
    