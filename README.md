# copyFilesRemote

I was backing up my files to a remote server using smb:server//. However, the server is disconnected from time to time. 
The script in this file checks the MD5 sums of the files between source and target. For any file, if the value is difference, then perform copy command

## Nextflow implementation
Ideally, I want to implement it in nextflow. However, I'm not sure how to check file existance and md5sum in a easy way. 

I think in later newer versions of nextflow, it might have this function as dicussed here: https://github.com/nextflow-io/nextflow/issues/2844

Currently, I only one nexf flow script for copy files in copyFilesRemote.nf
## Python implementation
I wrote a python script for this task.

### parameters
+ source: source file directory
+ target: target folder
+ p: regex patterns of the filenames you want to copy, such as ".*gz", ".*txt",etc
+ md5a: file that contain md5sum values for the source files. Default: None
+ md5b: file that contains md5sum values for the target files. Default: None
+ dryRun: whether dry-run or not? Default: True
To tun the script:

```bash
python copyFilesRemote_python.py /Users/yshang/Dropbox/github/copyFilesRemote/testDir/af testDir/bf --p '[ab].txt' --md5a testDir/af/md5sum.txt --md5b testDir/bf/md5sum.txt --dryRun False
# Or:
python copyFilesRemote_python.py /Users/yshang/Dropbox/github/copyFilesRemote/testDir/af testDir/bf --p '[ab].txt' --md5a testDir/af/md5sum.txt --md5b testDir/bf/md5sum.txt --dryRun F

```

Or if you want dry-run:

```bash
python copyFilesRemote_python.py /Users/yshang/Dropbox/github/copyFilesRemote/testDir/af testDir/bf --p '.*txt' --md5a testDir/af/md5sum.txt

```


```bash
python copyFilesRemote_python.py /Users/yshang/Dropbox/github/copyFilesRemote/testDir/af testDir/bf --p '.*txt' --md5a testDir/af/md5sum.txt --md5b testDir/af/md5sum.txt --dryRun True

```
