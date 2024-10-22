#!/usr/bin/env python3

from os.path import abspath

from shared.diff import checkForFilesNotInChecksum, checkForMissingAndChangedFiles
from shared.log import log, quit

def changes(args):
    sourceChecksumPath = abspath(args.checksum)

    filesNotInChecksum = checkForFilesNotInChecksum(sourceChecksumPath, args.PATHS, args.verbose != 0)
    keysToDelete, keysToAdd, changedKeys = checkForMissingAndChangedFiles(sourceChecksumPath, args.PATHS, args.verbose != 0)

    keysToAdd = set(filesNotInChecksum + keysToAdd)

    log(f"[{len(keysToDelete)}] missing  files")
    log(f"[{len(keysToAdd)}] files added")
    log(f"[{len(changedKeys)}] files changed")

    if len(keysToDelete) + len(changedKeys) + len(keysToAdd) > 0:
        quit(1)
    else:
        quit(0)

