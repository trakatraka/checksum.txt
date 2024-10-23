from os.path import exists, dirname, abspath, relpath, islink
from shared.fs import scanDir, shoudIgnore
from shared.checksum import readChecksumTXT, calculateChecksumTXTPathForKey, calculateChecksumTXTValueForKey, calculateChecksumTXTKeyForPath
from shared.log import logProgress, log, error, warn

def checkForMissingAndChangedFiles(checksumPath, paths=None, verbose=False):
    sourceChecksum = readChecksumTXT(checksumPath)
    keysToAdd = []
    keysToDelete = []
    changedKeys = []

    filesToCheck = []

    if paths == None:
        for key in sorted(sourceChecksum.keys()):
            filesToCheck.append(calculateChecksumTXTPathForKey(key, checksumPath))
    else:
        log(f"scanning for files")
        for path in paths:
            scanDir(path, filesToCheck)

    runned = 0
    total = len(filesToCheck)

    for file in sorted(filesToCheck):
        filepath = abspath(file)
        if not shoudIgnore(filepath, checksumPath):
            key = calculateChecksumTXTKeyForPath(filepath, checksumPath)
            if key not in sourceChecksum.keys():
                warn(f'[{key}] missing from checksum.txt!')
                keysToAdd.append(key)
            elif not exists(filepath) and not islink(filepath):
                error(f'[{key}] file not found!')
                keysToDelete.append(key)
            else:
                currentChecksum = calculateChecksumTXTValueForKey(key, checksumPath)
                if currentChecksum != sourceChecksum[key]:
                    error(f'[{key}] checksum validation failed !')
                    changedKeys.append((key, currentChecksum))
            runned+=1
            if verbose:
                logProgress(dirname(key), runned, total)
    
    return (keysToDelete, keysToAdd, changedKeys)

def checkForFilesNotInChecksum(checksumPath, paths=None, verbose=False):
    ret = []
    sourceChecksum = readChecksumTXT(checksumPath)

    filesToCheck = []

    log(f"scanning for files")

    if paths == None:
        scanDir(dirname(checksumPath), filesToCheck)
    else:
        for path in paths:
            scanDir(path, filesToCheck)
    
    runned = 0
    total = len(filesToCheck)
    
    for file in sorted(filesToCheck):
        path = abspath(file)
        if not shoudIgnore(path, checksumPath):
            key = calculateChecksumTXTKeyForPath(path, checksumPath)
            if key not in sourceChecksum.keys():
                error(f'[{key}] not in checksum.txt !')
                ret.append(key)
        runned+=1
        if verbose:
            logProgress(relpath(path, dirname(checksumPath)), runned, total)

    return ret