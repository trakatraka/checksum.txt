from os.path import abspath, join, relpath, curdir, isdir, dirname

from scripts.override import override
from shared.log import log, quit, error, logProgress, debug
from shared.checksum import readChecksumTXT, calculateChecksumTXTPathForKey, writeChecksumTXT
from shared.args import parser
from shared.fs import removePath, replacePath

def sync(args):
    sourceChecksumDirPath = abspath(args.source)
    targetChecksumDirPath = abspath(args.target)

    if not isdir(sourceChecksumDirPath):
        error(f"{args.source} not a dir!")
        quit(1)
    if not isdir(targetChecksumDirPath):
        error(f"{args.target} not a dir!")
        quit(1)

    log(f"{sourceChecksumDirPath} into {targetChecksumDirPath}")

    sourceChecksumPath = join(f"{sourceChecksumDirPath}", "checksum.txt")
    targetChecksumPath = join(f"{targetChecksumDirPath}", "checksum.txt")

    # regenerate checksum.txt on source and target
    if args.pre_sync == "all" or args.pre_sync == "source" or args.pre_sync == None:
        log(f"recalculating checkums for [{relpath(sourceChecksumPath, curdir)}]")
        override(parser.parse_args(["--checksum", sourceChecksumPath, "--dry-run", str(args.dry_run) if args.dry_run != None else "1", "override"]), True)
    if args.pre_sync == "all" or args.pre_sync == "target" or args.pre_sync == None:
        log(f"recalculating checkums for [{relpath(targetChecksumPath, curdir)}]")
        override(parser.parse_args(["--checksum", targetChecksumPath, "--dry-run", str(args.dry_run) if args.dry_run != None else "1", "override"]), True)

    # diff the 2 checksum.txt
    sourceChecksum = readChecksumTXT(sourceChecksumPath)
    targetChecksum = readChecksumTXT(targetChecksumPath)
    keysToDelete = []
    for targetKey in sorted(targetChecksum.keys()):
        if targetKey not in sourceChecksum:
            keysToDelete.append(targetKey)
    keysToAdd = []
    keysToReplace = []
    for sourceKey in sorted(sourceChecksum.keys()):
        if sourceKey not in targetChecksum:
            keysToAdd.append(sourceKey)
        elif sourceChecksum[sourceKey] != targetChecksum[sourceKey]:
                keysToReplace.append(sourceKey)

    # calculate mode
    deleteKeysMode = args.sync_mode == None or args.sync_mode == "delete" or args.sync_mode == "all"
    replaceKeysMode = args.sync_mode == None or args.sync_mode == "replace" or args.sync_mode == "all"
    addKeysMode = args.sync_mode == None or args.sync_mode == "add" or args.sync_mode == "all"

    # if deleteKeysMode and len(keysToDelete) > 0:
    #     log(f"[{len(keysToDelete)}] files to delete on target")
    # if replaceKeysMode and len(keysToReplace) > 0:
    #     log(f"[{len(keysToReplace)}] files to replace on target")
    # if addKeysMode and len(keysToAdd) > 0:
    #     log(f"[{len(keysToAdd)}] files to add to target")

    dryRunStr = f"" if args.dry_run == 0 else "NOT "
    totalChanges = (len(keysToDelete) if deleteKeysMode else 0) + (len(keysToReplace) if replaceKeysMode else 0) + (len(keysToAdd) if addKeysMode else 0)
    runnedChanges = 0
    log(f"{dryRunStr}syncing [{totalChanges}] changes")


    # first delete keys
    if deleteKeysMode:
        sortedKeys = sorted(set(keysToDelete))
        sortedKeys.reverse()
        for key in sortedKeys:
            debug(f"{dryRunStr}deleting [{key}] to target")
            targetFilePath = calculateChecksumTXTPathForKey(key, targetChecksumPath)
            if args.dry_run == 0:
                del targetChecksum[key]
                removePath(targetFilePath)
                writeChecksumTXT(targetChecksumPath, targetChecksum)
            runnedChanges+=1
            logProgress(dirname(key), runnedChanges, totalChanges)
    
    # second replace keys
    if replaceKeysMode:
        for key in sorted(set(keysToReplace)):
            debug(f"{dryRunStr}replacing [{key}] to target")
            sourceFilePath = calculateChecksumTXTPathForKey(key, sourceChecksumPath)
            targetFilePath = calculateChecksumTXTPathForKey(key, targetChecksumPath)
            if args.dry_run == 0:
                targetChecksum[key] = sourceChecksum[key]
                replacePath(sourceFilePath, targetFilePath)
                writeChecksumTXT(targetChecksumPath, targetChecksum)
            runnedChanges+=1
            logProgress(dirname(key), runnedChanges, totalChanges)

    # third add keys
    if addKeysMode:
        for key in sorted(set(keysToAdd)):
            debug(f"{dryRunStr}adding [{key}] to target")
            sourceFilePath = calculateChecksumTXTPathForKey(key, sourceChecksumPath)
            targetFilePath = calculateChecksumTXTPathForKey(key, targetChecksumPath)
            if args.dry_run == 0:
                targetChecksum[key] = sourceChecksum[key]
                replacePath(sourceFilePath, targetFilePath)
                writeChecksumTXT(targetChecksumPath, targetChecksum)
            runnedChanges+=1
            logProgress(dirname(key), runnedChanges, totalChanges)

    if deleteKeysMode:
        log(f"[{len(keysToDelete)}] files {dryRunStr}deleted on target")
    if replaceKeysMode:
        log(f"[{len(keysToReplace)}] files {dryRunStr}replaced on target")
    if addKeysMode:
        log(f"[{len(keysToAdd)}] files {dryRunStr}added to target")

    quit(0)

