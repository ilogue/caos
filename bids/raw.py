"""
Python script to gather dicom files and put them into a raw/ directory
"""
import os, glob, shutil
from os.path import join, expanduser

root = '/media/vandejjf/WDMyBook_Jasper/caos/'
acqdir = 'derya/presentation_files_allegra/CAOS_fMRT/'

print('Copying dcm directories to raw directory')
subjdirs = glob.glob(join(root, acqdir, '*'))
for s, subjdir in enumerate(subjdirs):
    inits = subjdir.split('/')[-1][:2]
    dcmdirs = [f for f in glob.glob(join(subjdir, '1.3.*')) if '.zip' not in f]
    if len(dcmdirs) == 1:
        dcmdirs = glob.glob(join(subjdir, dcmdirs[0], '1.3.*'))
    subjrawdir = join(root, 'raw', inits)
    msg = '\n{}/{} {} {}scans '.format(s+1, len(subjdirs), inits, len(dcmdirs))
    print(msg, end='', flush=True)
    for dcmdir in dcmdirs:
        print('.', end='', flush=True)
        number = os.path.basename(dcmdir)
        shutil.copytree(dcmdir, join(subjrawdir, number))
print('done')