@echo off

IF EXIST "G:\Backup\" (
    IF EXIST "C:\Users\shianchin\" (
    robocopy "C:\Users\shianchin\Documents" "G:\Backup\Documents" /MIR /DCOPY:T /xj /np /tee /log:backup_log.txt
    robocopy "C:\Users\shianchin\Pictures"  "G:\Backup\Pictures"  /MIR /DCOPY:T /xj /np /tee /log+:backup_log.txt
    robocopy "C:\Users\shianchin\Music"     "G:\Backup\Music"     /MIR /DCOPY:T /xj /np /tee /log+:backup_log.txt
    robocopy "C:\Users\shianchin\Downloads" "G:\Backup\Downloads" /MIR /DCOPY:T /xj /np /tee /log+:backup_log.txt
    ) ELSE (
    echo ERROR: Source directory "C:\Users\shianchin\" not found.
    )
) ELSE (
echo ERROR: Destination directory "G:\Backup\" not found.
)
pause