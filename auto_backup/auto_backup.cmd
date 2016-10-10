@echo off

IF EXIST "P:\Backup\" (
    IF EXIST "C:\Users\shianchin\" (
    robocopy "C:\Users\shianchin\Documents" "P:\Backup\Documents" /MIR /DCOPY:T /xj /np /tee /log:backup_log.txt
    robocopy "C:\Users\shianchin\Pictures"  "P:\Backup\Pictures"  /MIR /DCOPY:T /xj /np /tee /log+:backup_log.txt
    robocopy "C:\Users\shianchin\Music"     "P:\Backup\Music"     /MIR /DCOPY:T /xj /np /tee /log+:backup_log.txt
    robocopy "C:\Users\shianchin\Downloads" "P:\Backup\Downloads" /MIR /DCOPY:T /xj /np /tee /log+:backup_log.txt
    ) ELSE (
    echo ERROR: Source directory "C:\Users\shianchin\" not found.
    )
) ELSE (
echo ERROR: Destination directory "P:\Backup\" not found.
)
pause
