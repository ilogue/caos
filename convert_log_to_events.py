"""
Function to convert psychopy log to BIDS events file. See BIDS spec:

https://bids-specification.readthedocs.io/en/latest/04-modality-specific-files/05-task-events.html
https://bids-specification.readthedocs.io/en/latest/04-modality-specific-files/07-behavioral-experiments.html
"""
import pandas, mne
from numpy.testing import assert_array_equal


def check_row_valid(row):
    if row.ptype in ['INFO', 'WARNING']:
        return False
    messages = ['unnamed MovieStim', 'Created window', 'mouseVisible']
    for message in messages:
        if message in row.desc:
            return False
    return True


def trial_type(row):
    if 'Keypr' in row.desc:
        return 'response'
    elif 'nback' in row.desc:
        return 'nback'
    else:
        return row.desc.split(',')[2]


def duration(row):
    if row.trial_type == 'response':
        return 0.0
    else:
        return 3.0


def value(row):
    if row.trial_type == 'response':
        return 0
    else:
        return int(row.desc.split(',')[0])


def stim_name(row):
    if row.trial_type == 'response':
        return ''
    else:
        return row.desc.split(',')[1]


def convert_log_to_events(in_fpath, out_fpath):
    """BIDS events tsv from psychopy log 
    """
    df = pandas.read_csv(
        in_fpath,
        delimiter='\t',
        names=['onset', 'ptype', 'desc'],
        converters={'ptype': str.strip}
    )
    valid_rows = df.apply(check_row_valid, axis=1)
    df = df[valid_rows]
    df['trial_type'] = df.apply(trial_type, axis=1)
    df['duration'] = df.apply(duration, axis=1)
    df['value'] = df.apply(value, axis=1)
    df['stim_name'] = df.apply(stim_name, axis=1)
    df = df.drop(['ptype', 'desc'], axis=1)
    first_onset = df.iloc[0].onset
    df.onset -= first_onset

    # check if this behavior matches up with the corresponding eeg file
    eeg_path = out_fpath.replace('_events.tsv', '_eeg.edf')
    raw = mne.io.read_raw_edf(eeg_path, verbose='error')
    events = mne.find_events(raw, verbose='error')

    ## index only events that have triggers in eeg
    stimulus_events = df.trial_type != 'response'

    ## check if number of relevant events matches
    assert events.shape[0] == stimulus_events.sum()

    ## check if event values match
    assert_array_equal(events[:, 2], df[stimulus_events].value)

    ## onset should be  relative to first sample
    df.onset += events[0, 0] / raw.info['sfreq']

    # add sample column
    df['sample'] = None
    df.loc[stimulus_events, 'sample'] = events[:, 0]

    df.to_csv(out_fpath, sep='\t', index=False, float_format='%.8f')
    return df                                                                                                                         
