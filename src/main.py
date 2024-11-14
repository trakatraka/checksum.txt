#!/usr/bin/env -S python3 -B

from sys import argv
from os import curdir
from os.path import abspath

from shared.checksum import initHashWithArgs
from shared.args import parser
from scripts.validate import validate
from scripts.changes import changes
from scripts.override import override
from scripts.append import append
from scripts.sync import sync
from shared.log import error, quit, log, initLogWithArgs

args = parser.parse_args()
log(args)
log(f"PWD={abspath(curdir)}")
log(f"ARGS={argv[1:]}")
initLogWithArgs(args)
initHashWithArgs(args)

if args.CMD[0] == "sync":
    if args.target == None or args.source == None:
        error(f"--source and --target must be specified")
        quit(1)
    elif args.PATHS != None:
        error(f"PATHS cannot be specified with sync command")
        quit(1)
    else:
        sync(args)
else:
    if args.target != None or args.source != None:
        error(f"cannot use --source or --target without sync")
        quit(1)
    else:
        if args.CMD[0] == "validate":
            validate(args)
        elif args.CMD[0] == "changes":
            changes(args)
        elif args.CMD[0] == "append":
            append(args)
        elif args.CMD[0] == "override":
            override(args)