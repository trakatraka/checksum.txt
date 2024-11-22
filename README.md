# checksum.txt

small python script for managing a ```checksum.txt``` file for validating checksums.

```
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

## append

this command will only search for NEW files that are not registered in the ```checksum.txt``` file and add them.

```
$ checksum.txt append [PATHS]
```

## validate

this command will validate the files registered in the ```checksum.txt``` file.

```
$ checksum.txt validate [PATHS]
```

## override

this command will re calculate the checksum of the files registered in the ```checksum.txt``` file. With the optional **PATHS** argument you can only re-calculate the checksum for only some files.

```
$ checksum.txt override [PATHS]
```

## changes

this command will compare the files registered in ```checksum.txt``` with the actual files. With the optional **PATHS** argument you can only check for changes for only some files.

```
$ checksum.txt changes [PATHS]
```

## sync

this command will sync a source directory to a target directory.

```
$ checksum.txt sync --source <SOURCE> --target <TARGET>
```

### --sync-mode

the sync mode option can have the values ```all,delete,replace,add```.

- all: this means all operations will be performed.
- delete: this means only the delete operations will be performed.
- replace: this means only the replace files operations will be performed.
- add: this means only the add files operations will be performed.

### --pre-sync

the pre sync option can have the values ```all,source,target,none```.

- all: this means that the source and the target will have their's files checksum re-calculated before the sync.
- source: this means that only the source will have their's files checksum re-calculated before the sync.
- target: this means that only the target will have their's files checksum re-calculated before the sync.
- none: this disables calculating the checksum's before the sync.

## Other Options

### --dry-run

the --dry-run argument is for only simulating the actions that will be taken, NO changes will be made to the files or the ```checksum.txt``` file.

### --verbose

the --verbose argument is for adding additional logging output for debugging purposes.

### --do-not-scan

the --do-not-scan will disable the search for new files in the current command.

### --checksum

the --checksum argument is for specifing the actual ```checksum.txt``` file to be used. Its defaults to ```$PWD/checksum.txt```.

### LOG_FILE

if you set the env variable ```LOG_FILE``` a save log file will be used.

```
LOG_FILE=/tmp/checksum.txt.log checksum.txt validate
```

### Ignored Files

```.DS_Store``` and files that start with the ```._``` characters will be ignored.
