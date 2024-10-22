from os import listdir
from os.path import join, isdir, basename, islink

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