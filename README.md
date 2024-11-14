# checksum.txt

```bash
$ checksum.txt -h
usage: checksum.txt [-h] [--checksum [CHECKSUM]] [--hash [{sha1,sha256}]]
                    [--pre-sync [{all,source,target,none}]]
                    [--sync-mode [{all,delete,replace,add}]]
                    [--source [SOURCE]] [--target [TARGET]]
                    [--verbose [VERBOSE]] [--print-every [PRINT_EVERY]]
                    [--dry-run [DRY_RUN]] [--do-not-scan [DO_NOT_SCAN]]
                    {sync,validate,append,changes,override} [PATHS]

positional arguments:
  {sync,validate,append,changes,override}
                        the command to run
  PATHS                 a comma separated list of paths checksum.txt (default:
                        None)

optional arguments:
  -h, --help            show this help message and exit
  --checksum [CHECKSUM]
                        the checksum.txt file path (default: ./checksum.txt)
  --hash [{sha1,sha256}]
                        the hash setting for checksum.txt (default: sha256)
  --pre-sync [{all,source,target,none}]
                        the pre sync setting for checksum.txt (default: all)
  --sync-mode [{all,delete,replace,add}]
                        the sync setting for checksum.txt (default: all)
  --source [SOURCE]     the source setting for sync checksum.txt (default:
                        None)
  --target [TARGET]     the target setting for sync checksum.txt (default:
                        None)
  --verbose [VERBOSE]   the verbose setting for checksum.txt (default: 0)
  --print-every [PRINT_EVERY]
                        the print every setting for checksum.txt (default:
                        1000)
  --dry-run [DRY_RUN]   the dry-run setting for checksum.txt (default: 0)
  --do-not-scan [DO_NOT_SCAN]
                        disable scanning for new files (default: 0)
```
