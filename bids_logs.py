"""
Organize and convert the event log files to BIDS format
"""
import subprocess, glob, shutil, os
from os.path import join, expanduser, basename, isdir
from subject_ids import subject_ids
from logfile import PresentationLogfile

root = expanduser('~/Data/caos')
bidsdir = join(root, 'BIDS')

# Make sure we already have BIDS dir
assert isdir(bidsdir)

logfiles_localizer = glob.glob(join(root, 'logfiles_localizer', '*.log'))

## loop over subjects
for old_id, sub in subject_ids.items():
    print(f'\nSubject {sub} ({old_id})')
    loc_matches = list(filter(lambda f: basename(f)[:2] == old_id, logfiles_localizer))
    for fpath in loc_matches:
        logfile = PresentationLogfile(fpath)
        logfile.read()
        print(f'\t\tLogfile created {logfile.created}')
    if not len(loc_matches) == 1:
        print(f'\t[!] Found {len(loc_matches)} logfiles.')
## for localizer, print info on fmri created timing
## for localizer, print info on logfile created timing
## for exp, print info on fmri created timing
## for exp, print info on logfile created timing