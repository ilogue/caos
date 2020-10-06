# data prep: BIDS

Download MRIcroGL which includes compiled dcm2niix

https://www.nitrc.org/frs/download.php/10163/mricrogl_linux.zip//?i_agree=1&download_now=1

"Install" dcm2niix by linking it in /usr/bin
```
sudo ln -s <your github directory>/caos/bin/dcm2niix /usr/local/bin/dcm2niix
```

Run dcm2niix to see example output on one subject
```
dcm2niix /path/to/dicom/folder
```

- `raw.py` copy dicom directories to a simple *raw* directory
- run bids validator
- convert dicoms if necessary (dcm2bids)
- provide meta data
- run fmri prep

Susceptability Distortion correction. ("B0") We have acquired Point Spread Function (psf) data for this, but this is not supported by fmri-prep
http://fmriprep.readthedocs.io/en/latest/sdc.html#sdc

Approach for now; do not import psf files and try to do automated correction.

- http://miykael.github.io/nipype-beginner-s-guide/
- http://fmriprep.readthedocs.io/en/latest/
