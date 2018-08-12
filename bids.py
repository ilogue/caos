"""
Python script to gather data files and organize them into BIDS format
"""
import subprocess, os, glob, shutil
from os.path import join, expanduser

root = '/media/vandejjf/WDMyBook_Jasper/caos/'


# dcm2niix always looks for its config file in your home dir
# so we create a symbolic link to the file in this repository:
if not os.path.islink(expanduser('~/.dcm2nii.ini')):
    os.symlink('dcm2nii.ini', expanduser('~/.dcm2nii.ini'))

# subprocess.check_call(['echo','hallo'])


#os.mkdir(join(root, 'BIDS'))
