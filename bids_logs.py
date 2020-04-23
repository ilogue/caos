"""
Organize and convert the event log files to BIDS format

Assumes all runs on same day

## https://bids-specification.readthedocs.io/en/stable/04-modality-specific-files/05-task-events.html
"""
import subprocess, glob, shutil, os, time, json, datetime
from os.path import join, expanduser, basename, isdir, getsize
from subject_ids import subject_ids
from logfile import PresentationLogfile
from word_conditions import word_conditions
from word_translations import word_translations
from localizer_entities import localizer_entities
import pandas
pandas.options.mode.chained_assignment = None

FMR_MIN_MB = 5  ## ignore BOLD files smaller than this
## had a look and sound duration varies, 0.5-0.8
STIM_DUR = 0.5  ## sound duration for events file in sec, guessing for now
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
    
    for fpath in sub_log_fpaths:
        logfile = PresentationLogfile(fpath)
        logfile.read()
        sub_logs.append(logfile)
    sub_logs = sorted(sub_logs, key=lambda r: r.created)

    print(f'\t{len(sub_logs)} log files.')
    for log in sub_logs:
        log_fname = basename(log.fpath)
        print(f'\t\tstored {log.created}: {log_fname}')

    sub_fmrfiles = glob.glob(join(bidsdir, f'sub-{sub}', 'func', '*_bold.json'))
    
    sub_fmr_runs_valid = []
    for fpath in sub_fmrfiles:
        with open(fpath) as fhandle:
            fmr_meta = json.load(fhandle)
        aq_time = datetime.datetime.strptime(fmr_meta['AcquisitionTime'], '%H:%M:%S.%f')
        ## assume fmr recorded on the date stamped in logfile:
        aq_time = datetime.datetime.combine(logfile.created, aq_time.time()).replace(microsecond=0)
        size_mb = getsize(fpath.replace('.json', '.nii.gz')) / (1024 * 1024)
        if size_mb > FMR_MIN_MB:
            sub_fmr_runs_valid.append(dict(fpath=fpath, aq_time=aq_time, size_mb=size_mb))
    sub_fmr_runs_valid = sorted(sub_fmr_runs_valid, key=lambda r: r['aq_time'])

    print(f'\t{len(sub_fmr_runs_valid)} fmr files larger than {FMR_MIN_MB}mb.')
    for fmr_run in sub_fmr_runs_valid:
        fmr_fname = basename(fmr_run['fpath'])
        print(f'\t\tstarted {fmr_run["aq_time"]}, size {fmr_run["size_mb"]:.1f}MB: {fmr_fname}')

    print('')
    for r, fmr_run in enumerate(sub_fmr_runs_valid, start=1):
        ## find logfile match for a given run
        ten_mins = datetime.timedelta(minutes=10)
        log = min(sub_logs, key=lambda log: abs(log.created - fmr_run['aq_time'] - ten_mins))
        fmr_fname = basename(fmr_run['fpath'])
        log_fname = basename(log.fpath)
        print(f'\tmatch {r} of {len(sub_fmr_runs_valid)}:\n\t\t{fmr_fname}\n\t\t{log_fname}')

        fpath_evt = fmr_run['fpath'].replace('_bold.json', '_events.tsv')
        df = log.to_dataframe()
        ## see "convert_log_to_events.py"
        df = df[['Event_Type', 'Code', 'Time']]
        ## get time of first volume in ms/10
        t0 = df[df.Event_Type=='Pulse'].iloc[0].Time
        ## onset should be relative to first volume:
        df.Time = df.Time - t0
        df.Time = df.Time / (10*1000)

        if log.scenario == 'CAOS_main':
            assert 'task-exp' in fpath_evt, 'presentation scenario and BIDS task name dont match'
            df = df[df.Event_Type == 'Sound']
            fname = df.Code.str.split("\\").str.get(-1)
            word_german = fname.str.split('.').str.get(0)
            df['entity'] = word_german.apply(lambda g: word_translations[g])
            df['task_type'] = word_german.apply(lambda g: word_conditions[g])
            df['stim_file'] = fname.apply(lambda f: join('stimuli', 'images', f))
            df['duration'] = STIM_DUR
        elif log.scenario == 'LOC-localizer_1':
            assert 'task-loc' in fpath_evt, 'presentation scenario and BIDS task name dont match'
            df = df[df.Event_Type == 'Picture']
            df = df[~(df.Code == 'fixation_cross')]
            fname = df.Code.str.strip()
            object_index = fname.str.split('.').str.get(0).str.split('_').str.get(0)
            cond_index = fname.str.split('.').str.get(0).str.split('_').str.get(1)
            conditions = {1: 'object', 2: 'object_scrambled', 3: 'shape', 4: 'shape_scrambled'}
            df['entity'] = object_index.apply(lambda o: localizer_entities[int(o)])
            df['task_type'] = cond_index.apply(lambda c: conditions[int(c)])
            df['stim_file'] = fname.apply(lambda f: join('stimuli', 'pictures', f))
            df['duration'] = 3
        else:
            print(f'Unknown scenario: {log.scenario}')
        df = df.rename(columns=dict(Time='onset'))
        df = df.drop(['Code', 'Event_Type'], axis=1)
        df.to_csv(fpath_evt, sep='\t', index=False, float_format='%.3f')

