# Windows script file for auto backup
Make use of robocopy (Robust File Copy) to make a mirror backup.

Syntax:

```robocopy <Source> <Destination> [<File>[ ...]] [<Options>]```

Options used explained:

/MIR - Mirrors a directory tree (equivalent to /e plus /purge).

/DCOPY:T - Copies directory time stamps.

/xj - Excludes junction points.

/np - Specifies that the progress of the copying operation (the number of files or directories copied so far) will not be displayed.

/tee - Writes the status output to the console window, as well as to the log file.

/log:backup_log.txt - Writes the status output to the log file (overwrites the existing log file).

/log+:backup_log.txt - Writes the status output to the log file (appends the output to the existing log file).
