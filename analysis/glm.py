"""Helper functions to get voxel activity patterns with a GLM

Wraps functions from pyGLMdenoise
"""
import numpy
from glmdenoise.utils.gethrf import getcanonicalhrf
from glmdenoise.utils.make_design_matrix import make_design as gd_make_design
from glmdenoise.whiten_data import whiten_data as gd_whiten_data

def make_design(events, n_vols, tr):
    events['trial_type'] = events.entity
    stim_dur = numpy.median(events.duration)
    hrf = getcanonicalhrf(stim_dur, tr)
    return gd_make_design(events, tr, n_vols, hrf)


def whiten_data(data, design):
    wdata_list, wdesign_list = gd_whiten_data([data], [design])
    return wdata_list[0], wdesign_list[0]

# fit_runs (get betas)