from os.path import exists, dirname, abspath, islink
from shared.fs import scanDir, shoudIgnore
from shared.checksum import calculateChecksumTXTPathForKey, calculateChecksumTXTValueForKey, calculateChecksumTXTKeyForPath
from shared.log import logProgress, log, error, verboseWarn, debug, warn
from time import time

def checkChanges(checksumPath, checksum, args):
    filesNotInChecksum = checkForFilesNotInChecksum(checksumPath, checksum, args.PATHS) if args.do_not_scan == 0 else []
    
    keysToDelete, keysToAdd, changedKeys, errorKeys = checkForMissingAndChangedFiles(checksumPath, checksum, args.PATHS)

    keysToAdd = set(filesNotInChecksum + keysToAdd)

    return keysToDelete, keysToAdd, changedKeys, errorKeys

def checkForMissingAndChangedFiles(checksumPath, checksum, paths=None):
    #sourceChecksum = readChecksumTXT(checksumPath)
    keysToAdd = []
    keysToDelete = []
    changedKeys = []
    errorKeys = []

    filesToCheck = []

    if paths == None:
        for key in sorted(checksum.keys()):
            filesToCheck.append(calculateChecksumTXTPathForKey(key, checksumPath))
    else:
        MS_FROM_START = int(round(time() * 1000))
        log(f"scanning for files")
        for path in paths:
            scanDir(path, filesToCheck)
        took = int(round(time() * 1000)) - MS_FROM_START
        log(f"scanning for files took {took}ms")

    runned = 0
    total = len(filesToCheck)

    MS_FROM_START = int(round(time() * 1000))

    log(f"checking {total} checksums")

    for file in sorted(filesToCheck):
        filepath = abspath(file)
        if not shoudIgnore(filepath, checksumPath):
            key = calculateChecksumTXTKeyForPath(filepath, checksumPath)
            if key not in checksum.keys():
                warn(f'[{key}] not in checksum.txt!')
                keysToAdd.append(key)
            elif not exists(filepath) and not islink(filepath):
                warn(f'[{key}] file not found!')
                keysToDelete.append(key)
            else:
                try:
                    currentChecksum = calculateChecksumTXTValueForKey(key, checksumPath)
                    if currentChecksum != checksum[key]:
                        warn(f'[{key}] checksum changed !')
                        changedKeys.append((key, currentChecksum))
                except Exception as e:
                    error(e)
                    error(f'[{key}] error calculating checksum for {key} !')
                    errorKeys.append(key)
            runned+=1
            logProgress(dirname(key), runned, total)
    
    took = int(round(time() * 1000)) - MS_FROM_START
    log(f"checking {total} checksums took {took}ms")
    
    return (keysToDelete, keysToAdd, changedKeys, errorKeys)

def checkForFilesNotInChecksum(checksumPath, checksum, paths=None):
    MS_FROM_START = int(round(time() * 1000))
    ret = []

    filesToCheck = []

    log(f"scanning for files not in checksum.txt")

    if paths == None:
        scanDir(dirname(checksumPath), filesToCheck)
    else:
        for path in paths:
            scanDir(path, filesToCheck)
    
    #runned = 0
    #total = len(filesToCheck)
    
    for file in sorted(filesToCheck):
        path = abspath(file)
        if not shoudIgnore(path, checksumPath):
            key = calculateChecksumTXTKeyForPath(path, checksumPath)
            if key not in checksum.keys():
                debug(f'[{key}] not in checksum.txt !')
                ret.append(key)
        #runned+=1
        #if verbose:
        #    logProgress(relpath(path, dirname(checksumPath)), runned, total)
    took = int(round(time() * 1000)) - MS_FROM_START
    log(f"found [{len(ret)}] files not in checksum.txt")
    log(f"scanning for files not in checksum.txt took {took}ms")

    return ret

def checkForMissingFilesInChecksum(checksumPath, checksum):
    MS_FROM_START = int(round(time() * 1000))
    ret = []

    filesToCheck = sorted(checksum.keys())

    log(f"scanning for missing files in checksum.txt")
    
    runned = 0
    total = len(filesToCheck)
    
    for key in sorted(filesToCheck):
        path = abspath(key)
        if not exists(path) or shoudIgnore(path, checksumPath):
            warn(f'[{key}] missing in checksum.txt !')
            ret.append(key)
        runned+=1
        logProgress(dirname(key), runned, total)

    took = int(round(time() * 1000)) - MS_FROM_START
    log(f"found [{len(ret)}] missing files in checksum.txt")
    log(f"scanning for missing files in checksum.txt took {took}ms")

    return ret