"""
Organize and convert the event log files to BIDS format
"""
import subprocess, glob, shutil, os, time, json, datetime
from os.path import join, expanduser, basename, isdir
from subject_ids import subject_ids
from logfile import PresentationLogfile

root = expanduser('~/Data/caos')
bidsdir = join(root, 'BIDS')

# Make sure we already have BIDS dir
assert isdir(bidsdir)

logfiles_localizer = glob.glob(join(root, 'logfiles_localizer', '*.log'))
logfiles_experiment = glob.glob(join(root, 'logfiles_experiment', '*.log'))
all_logfiles = logfiles_localizer + logfiles_experiment

## loop over subjects
for old_id, sub in subject_ids.items():
    print(f'\n\nSubject {sub} ({old_id})')

    sub_logfiles = list(filter(lambda f: basename(f)[:2] == old_id, all_logfiles))
    print(f'\t{len(sub_logfiles)} log files.')

    for fpath in sub_logfiles:
        logfile = PresentationLogfile(fpath)
        logfile.read()
        print(f'\t\tLogfile created {logfile.created}')

    sub_fmrfiles = glob.glob(join(bidsdir, f'sub-{sub}', 'func', '*_bold.json'))
    print(f'\t{len(sub_fmrfiles)} fmr files.')
    for fpath in sub_fmrfiles:
        with open(fpath) as fhandle:
            fmr_meta = json.load(fhandle)
        aq_time = datetime.datetime.strptime(fmr_meta['AcquisitionTime'], '%H:%M:%S.%f')
        print(f'\t\tFmr created {aq_time}')
