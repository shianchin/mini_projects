robocopy C:\Users\user\Documents F:\Backup\Documents /MIR /DCOPY:T /xj /np /tee /log:backup_log.txt
robocopy C:\Users\user\Pictures  F:\Backup\Pictures  /MIR /DCOPY:T /xj /np /tee /log+:backup_log.txt
robocopy C:\Users\user\Music     F:\Backup\Music     /MIR /DCOPY:T /xj /np /tee /log+:backup_log.txt
robocopy C:\Users\user\Downloads F:\Backup\Downloads /MIR /DCOPY:T /xj /np /tee /log+:backup_log.txt
pause