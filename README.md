# copyFilesRemote

I was backing up my files to a remote server using smb:server//. However, the server is disconnected from time to time. 
The script in this file checks the MD5 sums of the files between source and target. For any file, if the value is difference, then perform copy command
