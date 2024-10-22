#!/usr/bin/env python3

from os.path import abspath

from shared.diff import checkForFilesNotInChecksum, checkForMissingAndChangedFiles
from shared.checksum import calculateChecksumTXTValueForKey, readChecksumTXT, writeChecksumTXT
from shared.log import log, quit

def override(args, noQuiting=False):
    sourceChecksumPath = abspath(args.checksum)

    sourceChecksum = readChecksumTXT(sourceChecksumPath)

    filesNotInChecksum = checkForFilesNotInChecksum(sourceChecksumPath, args.PATHS, args.verbose != 0)
    keysToDelete, keysToAdd, changedKeys = checkForMissingAndChangedFiles(sourceChecksumPath, args.PATHS, args.verbose != 0)

    keysToAdd = set(filesNotInChecksum + keysToAdd)

    for key in keysToDelete:
        log(f'{key} removing from checksum.txt!')
        del sourceChecksum[key]
    
    for key in keysToAdd:
        value = calculateChecksumTXTValueForKey(key, sourceChecksumPath)
        log(f'{key} adding to checksum.txt!')
        sourceChecksum[key] = value

    for (key, checksum) in changedKeys:
        log(f'{key} updating from checksum.txt!')
        sourceChecksum[key] = checksum

    log(f"[{len(keysToDelete)}] missing files")
    log(f"[{len(keysToAdd)}] files added")
    log(f"[{len(changedKeys)}] files changed")

    if args.dry_run == 0:
        log(f"writing changes to checksum.txt")
        writeChecksumTXT(sourceChecksumPath, sourceChecksum)
        if not noQuiting:
            quit(0)
    else:
        log(f"not writing changes to checksum.txt")
        if not noQuiting:
            quit(0)