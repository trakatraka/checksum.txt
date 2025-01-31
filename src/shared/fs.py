from os import listdir, unlink, rmdir, remove, symlink, readlink, makedirs, mkdir
from os.path import join, isdir, basename, islink, exists, dirname

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
    return path == checksumPath or basename(path) == "Icon\r" or basename(path) == ".DS_Store" or (not isdir(path) and len(basename(path)) > 2 and basename(path)[0:2] == "._")

def removePath(path):
    if islink(path):
        unlink(path)
    elif isdir(path):
        rmtree(path, ignore_errors=True)
    elif exists(path):
        remove(path)

def replacePath(sourceFilePath, targetFilePath):
    removePath(targetFilePath)
    targetDirname = dirname(targetFilePath)
    if not exists(targetDirname):
        makedirs(targetDirname, exist_ok=False)
    if islink(sourceFilePath):
        symlink(readlink(sourceFilePath), targetFilePath)
    elif isdir(sourceFilePath):
        mkdir(targetFilePath)
    else:
        copyfile(sourceFilePath, targetFilePath)