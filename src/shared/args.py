from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from pathlib import Path

def list_of_paths(arg):
    split = arg.split(',')
    ret = []
    for p in split:
        ret.append(Path(p))
    return ret

parser = ArgumentParser(
    prog='checksum.txt',
    formatter_class=ArgumentDefaultsHelpFormatter)

parser.add_argument('--pre-sync', nargs='?', choices=["checksum", "source_checksum", "target_checksum", "none"], default="checksum", help='the pre sync setting for %(prog)s (default: %(default)s)')
parser.add_argument('--sync-mode', nargs='?', choices=["delete_replace_add", "delete", "replace", "add", "delete_replace", "replace_add", "delete_add"], default="delete_replace_add", help='the sync setting for %(prog)s (default: %(default)s)')
parser.add_argument('--verbose', nargs='?', type=int, default=0, help='the verbose setting for %(prog)s (default: %(default)s)')
parser.add_argument('--source', nargs='?', type=Path, default=None, help='the source setting for sync %(prog)s (default: %(default)s)')
parser.add_argument('--target', nargs='?', type=Path, default=None, help='the target setting for sync %(prog)s (default: %(default)s)')
parser.add_argument('--dry-run', nargs='?', type=int, default=0, help='the dry-run setting for %(prog)s (default: %(default)s)')
parser.add_argument('--checksum', nargs='?', type=Path, default="./checksum.txt", help='the checksum.txt file path (default: %(default)s)')
parser.add_argument('CMD', nargs=1, choices=['sync', 'validate', 'append', 'changes', 'override'], help='the command to run')
parser.add_argument('PATHS', nargs='?', type=list_of_paths, default=None, help='a comma separated list of paths %(prog)s (default: %(default)s)')