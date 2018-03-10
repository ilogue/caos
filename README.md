# caos
CAOS project

Setup python
```
virtualenv -p python3 env
```

Download MRIcroGL which includes compiled dcm2niix

https://www.nitrc.org/frs/download.php/10163/mricrogl_linux.zip//?i_agree=1&download_now=1

"Install" dcm2niix by linking it in /usr/bin
```
sudo ln -s /home/jasper/Software/mricrogl_lx/dcm2niix /usr/local/bin/dcm2niix
```

Run dcm2niix to see example output on one subject
```
dcm2niix /path/to/dicom/folder
```

http://miykael.github.io/nipype-beginner-s-guide/
fmri prep:
http://fmriprep.readthedocs.io/en/latest/


- run bids validator
- convert dicoms if necessary (dcm2bids)
- provide meta data
- run fmri prep

Susceptability Distortion correction. ("B0") We have acquired Point Spread Function (psf) data for this, but this is not supported by fmri-prep
http://fmriprep.readthedocs.io/en/latest/sdc.html#sdc

Approach for now; do not import psf files and try to do automated correction.
