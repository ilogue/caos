"""Helper functions to get voxel activity patterns with a GLM

Wraps functions from pyGLMdenoise
"""
import numpy
from glmdenoise.utils.gethrf import getcanonicalhrf
from glmdenoise.utils.make_design_matrix import make_design as gd_make_design

def make_design(events, n_vols, tr):
    events['trial_type'] = events.entity
    stim_dur = numpy.median(events.duration)
    hrf = getcanonicalhrf(stim_dur, tr)
    return gd_make_design(events, tr, n_vols, hrf)

##TODO:
# whiten_data
# fit_runs (get betas)