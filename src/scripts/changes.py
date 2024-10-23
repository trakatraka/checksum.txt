#!/usr/bin/env python3

from os.path import abspath

from shared.diff import checkChanges
from shared.log import log, quit

def changes(args):
    sourceChecksumPath = abspath(args.checksum)

    keysToDelete, keysToAdd, changedKeys = checkChanges(sourceChecksumPath, args)

    log(f"[{len(keysToDelete)}] missing  files")
    log(f"[{len(keysToAdd)}] files added")
    log(f"[{len(changedKeys)}] files changed")

    if len(keysToDelete) + len(changedKeys) + len(keysToAdd) > 0:
        quit(1)
    else:
        quit(0)

