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
        log(f'{key} removing from checksum.txt!')
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
    
    for errorKey in errorKeys:
        debug(f"error reading [{errorKey}]")

    log(f"[{len(keysToDelete)}] files deleted")
    log(f"[{len(keysToAdd)}] files added")
    log(f"[{len(changedKeys)}] files changed")
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