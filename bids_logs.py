"""
Organize and convert the event log files to BIDS format

Assumes all runs on same day
"""
import subprocess, glob, shutil, os, time, json, datetime
from os.path import join, expanduser, basename, isdir, getsize
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

    sub_log_fpaths = list(filter(lambda f: basename(f)[:2] == old_id, all_logfiles))
    sub_logs = []
    print(f'\t{len(sub_log_fpaths)} log files.')
    for fpath in sub_log_fpaths:
        logfile = PresentationLogfile(fpath)
        logfile.read()
        sub_logs.append(logfile)
        print(f'\t\tLogfile created {logfile.created}')

    sub_fmrfiles = glob.glob(join(bidsdir, f'sub-{sub}', 'func', '*_bold.json'))
    print(f'\t{len(sub_fmrfiles)} fmr files.')
    sub_fmr_runs_valid = []
    for fpath in sub_fmrfiles:
        with open(fpath) as fhandle:
            fmr_meta = json.load(fhandle)
        aq_time = datetime.datetime.strptime(fmr_meta['AcquisitionTime'], '%H:%M:%S.%f')
        ## assume fmr recorded on date stamped in logfile:
        aq_time = datetime.datetime.combine(logfile.created, aq_time.time()).replace(microsecond=0)
        size_mb = getsize(fpath.replace('.json', '.nii.gz')) / (1024 * 1024)
        if size_mb > 1:
            print(f'\t\tFmr created {aq_time}, size {size_mb:.1f}MB')
            sub_fmr_runs_valid.append(dict(fpath=fpath, aq_time=aq_time))
        else:
            print(f'\t\t(Ignoring fmr created {aq_time}, size {size_mb:.1f}MB)')
    sub_fmr_runs_valid = sorted(sub_fmr_runs_valid, key=lambda r: r['aq_time'])

    print('')
    for r, fmr_run in enumerate(sub_fmr_runs_valid, start=1):
        ## find logfile match for a given run
        ten_mins = datetime.timedelta(minutes=10)
        matched_log = min(sub_logs, key=lambda log: abs(log.created - fmr_run['aq_time'] - ten_mins))
        fmr_fname = basename(fmr_run['fpath'])
        log_fname = basename(matched_log.fpath)
        print(f'\tmatch {r} of {len(sub_fmr_runs_valid)}:\n\t\t{fmr_fname}\n\t\t{log_fname}')


# def nearest(items, pivot):
#     return min(items, key=lambda x: abs(x - pivot))
