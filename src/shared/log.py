from math import floor, ceil
from os import environ, _exit, getpid
from time import time
from logging import getLogger, basicConfig, DEBUG

logger = None

if environ.get("LOG_FILE") != None:
    logger = getLogger("")
    basicConfig(filename=environ.get("LOG_FILE"), encoding='utf-8', level=DEBUG, format=f'%(asctime)s [{getpid()}] [%(levelname)s] %(message)s')

PRINT_EVERY = 1000

MS_FROM_START = int(round(time() * 1000))

verboseSetting = False
def setVerbose(value: bool=False):
    global verboseSetting
    verboseSetting = value

def getVerbose():
    return verboseSetting

def msFromStart():
    return int(round(time() * 1000)) - MS_FROM_START

def logProgress(lastDir: str, runned: int, TOTAL: int):
    if runned % PRINT_EVERY == 0:
        p = floor(((runned / TOTAL) * 100) * 100) / 100
        took = msFromStart()
        elapsed = ceil(took / 1000)
        timeLeftAprox = ceil(ceil((took / runned) * (TOTAL - runned) / 1000) / 60)
        totalTimeAprox = ceil(ceil((took / runned) * (TOTAL) / 1000) / 60)
        perFileAprox = ceil((took / runned) * 1000) / 1000
        log(f"[{p}]% {runned}/{TOTAL} elapsed time [{elapsed}]s time left aprox [{timeLeftAprox}/{totalTimeAprox}]m per file aprox [{perFileAprox}]ms last dir [{lastDir}]")

def debug(str):
    if getVerbose():
        print(str)
    if logger != None:
        logger.debug(str)  

def log(str):
    print(str)
    if logger != None:
        logger.info(str)

def verboseError(str):
    if getVerbose():
        print(f"[ERROR] {str}")
    if logger != None:
        logger.error(str)

def error(str):
    print(f"[ERROR] {str}")
    if logger != None:
        logger.error(str)

def warn(str):
    print(f"[warn] {str}")
    if logger != None:
        logger.warning(str)

def quit(code):
    took = msFromStart()
    if code != 0:
        log(f"took {took}ms")
        error(f"exiting with code: [{code}]")
        log(f"")
        _exit(code)
    else:
        log(f"took {took}ms")
        log(f"")
        _exit(0)