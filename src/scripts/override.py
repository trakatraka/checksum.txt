#!/usr/bin/env python3

from os.path import abspath

from shared.diff import checkChanges
from shared.checksum import calculateChecksumTXTValueForKey, readChecksumTXT, writeChecksumTXT
from shared.log import log, quit, error, debug

def override(args, noQuiting=False):
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

    for key in keysToDelete:
        debug(f'{key} removing from checksum.txt!')
        del(sourceChecksum[key])
    
    for key in keysToAdd:
        try:
            value = calculateChecksumTXTValueForKey(key, sourceChecksumPath)
            debug(f'{key} adding to checksum.txt!')
            sourceChecksum[key] = value
        except Exception:
            error(f"error calculating ")

    for (key, checksum) in changedKeys:
        debug(f'{key} updating from checksum.txt!')
        sourceChecksum[key] = checksum

    log(f"[{len(keysToDelete)}] files deleted")
    log(f"[{len(changedKeys)}] files changed")
    log(f"[{len(keysToAdd)}] files added")
    if len(errorKeys) > 0:
        error(f"[{len(errorKeys)}] files cannot be read!")

    if args.dry_run == 0:
        log(f"writing changes to checksum.txt")
        writeChecksumTXT(sourceChecksumPath, sourceChecksum)
        if not noQuiting:
            quit(0 if len(errorKeys) == 0 else 1)
    else:
        log(f"not writing changes to checksum.txt")
        if not noQuiting:
            quit(0 if len(errorKeys) == 0 else 1)