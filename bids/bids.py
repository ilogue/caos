"""
Python script to organize raw data according to BIDS format
"""
import subprocess, os, glob, shutil
from os.path import join, expanduser
from dcm2bids.dcm2bids import Dcm2bids

root = '/media/vandejjf/WDMyBook_Jasper/caos/'
bidsdir = join(root, 'BIDS')

# Make sure we are not overwriting existing BIDS dir
assert not os.path.isdir(bidsdir)
# Make sure dcm2niix binary is linked in /usr/local/bin/
assert os.path.islink('/usr/local/bin/dcm2niix')
# dcm2niix always looks for its config file in your home dir
assert os.path.islink(expanduser('~/.dcm2nii.ini'))

settings = dict(
    config='dcm2bids.json', # "JSON configuration file (see example/config.json)",
    clobber=True,           # Overwrite files
    outputdir=bidsdir,      # "Output BIDS study directory (default current directory)",
    loglevel='INFO',       # "Set logging level (the log file is written to outputdir)"
)

subjdcmdirs = glob.glob(join(root, 'raw', '*'))
for s, subjdir in enumerate(subjdcmdirs):
    print('\n\n\n##########\nSubject {}\n##########\n'.format(s+1))
    converter = Dcm2bids(dicom_dir=[subjdir], participant=s+1, **settings)
    converter.run()

# Dcm2Bids dcm2niix command:
# dcm2niix -b y -ba y -z y -f '%f_%p_%t_series%3s' -o /media/vandejjf/WDMyBook_Jasper/caos/BIDS/tmp_dcm2bids/sub-1 /
