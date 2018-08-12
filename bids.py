"""
Python script to gather data files and organize them into BIDS format
"""
import subprocess, os, glob, shutil
from os.path import join, expanduser
from dcm2bids.dcm2bids import Dcm2bids

root = '/media/vandejjf/WDMyBook_Jasper/caos/'
bidsdir = join(root, 'BIDS')

# Make sure we are not overwriting existing BIDS dir
assert not os.path.isdir(join(root, 'BIDS'))
# Make sure dcm2niix binary is linked in /usr/local/bin/
assert os.path.islink('/usr/local/bin/dcm2niix')
# dcm2niix always looks for its config file in your home dir
assert os.path.islink(expanduser('~/.dcm2nii.ini')

settings = dict(
    config='dcm2bids.json', # "JSON configuration file (see example/config.json)",
    outputdir=bidsdir, # "Output BIDS study directory (default current directory)",
    loglevel='INFO', # "Set logging level (the log file is written to outputdir)"
)

subjdcm = join(root, 'raw', 'AS')
converter = Dcm2bids(dicom_dir=subjdcm, participant=None, **settings)
converter.run()
