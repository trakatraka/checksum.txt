from os import listdir, unlink, rmdir, remove, symlink, readlink, mkdir
from os.path import join, isdir, basename, islink, exists

from shutil import copyfile, rmtree

def scanDir(dir, ret=None):
    if ret == None:
        ret = []
    files = listdir(dir)
    for name in files:
        path = join(dir, name)
        ret.append(path)
        if isdir(path) and not islink(path):
            scanDir(path, ret)
    return ret

def getFilesOfList(paths):
    ret = []
    for path in paths:
        if isdir(path) and not islink(path):
            scanDir(path, ret)
        else:
            ret.append(path)
    return ret

def shoudIgnore(path, checksumPath):
    return path == checksumPath or basename(path) == ".DS_Store"

def removePath(path):
    if islink(path):
        unlink(path)
    elif isdir(path):
        rmtree(path, ignore_errors=True)
    elif exists(path):
        remove(path)

def replacePath(sourceFilePath, targetFilePath):
    removePath(targetFilePath)
    if islink(sourceFilePath):
        symlink(readlink(sourceFilePath), targetFilePath)
    elif isdir(sourceFilePath):
        mkdir(targetFilePath)
    else:
        copyfile(sourceFilePath, targetFilePath)