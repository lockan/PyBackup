import sys
import os.path
import time
import subprocess

# DEFINE VARS
robocopy_cmd = "robocopy" 
robocopy_args = "/MIR /R:5 /W:5 /ZB /NFL /NDL"

# !!! DEFINE BACKUP FOLDER PATHS !!!
# IMPORTANT: Use / instead of \
paths = {
    "D:/BCIT", 
    "D:/Documents",
    "D:/Dropbox",
    "D:/Projects",
    "D:/RCDrone",
    "E:/Media/Lockhart Music",
    "E:/Media/Music",
    "E:/Media/Other Music/_Digital Albums",
    "E:/Media/Other Music/_Downloads",
    "E:/Media/Other Music/_Misc",
    "E:/Media/Other Music/_Soundtracks",
    "E:/Media/Pictures",
    "E:/Media/Videos/NIN Stuff",
    "E:/Media/Videos/RunCam2",
}
# !!! DEFINE TARGET DRIVE LETTER FOR BACKUP !!!
drive = "J:"

# SCRIPT FUNCTIONS
def usage():
    print "\n ==== PyBackup Usage ===="
    print " PyBackup"
    print " Please edit the script to specify Backup Source paths and Target drive letter"
    print " Windows paths must be specified using forward slashes ( '/' )"
    print " PyBackup must be run with elevated access priveleges!!"
    print
    exit(1)

def validateTargetDrive(target):
    if len(target) != 2: 
        return None

    if target[1] != ":" : 
        return None

    if os.path.exists(target): 
        return target
    else:
        return None

def getDest(source, target): 
    sourcedrive = source.split(':')[0] + ":"
    dest = source.replace(sourcedrive, target)
    return dest

def backup(source, dest, logname):
    print "\n===== Backing up " + source + " to " + dest + " ====="
    #forcing enclosing quotes on source and dest to handle paths that contain spaces
    backupcmd = robocopy_cmd + " \"" + source + "\" \"" + dest + "\" " + robocopy_args + " /LOG+:" + logname + " /TEE"
    print backupcmd
    try: 
        proc = subprocess.Popen(backupcmd, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False, bufsize=1)
        out, err = proc.communicate()
        if out != None: print out 
        if err != None: print err
        
        #Check robocopy error codes
        #Robocopy uses both 0 and 1 for success states; Anything greater than 1 indicates something may have gone wrong.
        exitcode = proc.returncode
        if exitcode >= 2: 
            print "\n !!! WARNING: Errors may have occurred while backing up folder " + source
            return 1
        else:
            return 0
    
    except Exception as ex: 
        print "\n !!! ERROR: Exception encountered"
        print ex.message

# ===== MAIN LOOP ======
def main():        
    targetdrive = validateTargetDrive(drive)
    if targetdrive == None: 
        print "\n!!! Error: Unable to locate specified backup drive letter. Please check the script."
        usage()

    if len(paths) == 0: 
        print "\n!!! Error: no backup source paths defined. Please define the paths to back up in the script."
        usage()

    print "==== Running PyBackup ===="

    c_errors = 0
    c_badpaths = 0
    badpaths = []
    logpath = targetdrive + "/" + "backup_" + time.strftime("%m-%d-%y_%H-%M-%S") + ".log"

    for source in paths: 
        #validate source path
        if not os.path.exists(source):
            print "\n!!! WARNING: could not locate path: " + source
            c_badpaths += 1
            badpaths.append(source)
            continue
        
        # map source path to destination path
        dest = getDest(source, targetdrive)
        retcode = backup(source, dest, logpath)
        if retcode > 0: 
            c_errors += 1

    print "\n ==== BACKUP PROCESS FINISHED ===="
    print "See Backup log for details: " + logpath

    if c_badpaths > 0: 
        print "\n!!! WARNING: could not locate some of the specified backup paths:"
        for p in badpaths: print "  " + p
        print "Please check your paths list to verify that all are correct and exist."
        exit(1)

    if c_errors > 0: 
        print "\n!!! WARNING: Errors occurred while copying some paths. "
        print "Please consult the backup log."
        exit(1)
        
    exit(0)

if __name__ == "__main__":
    main()
