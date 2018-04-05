#!python
# -*- coding: utf-8 -*-#
#
# Author      : Bhishan Poudel; Physics Graduate Student, Ohio University
# Date        :  Mar 21, 2018
# 
# Imports
import os
import subprocess
import glob
import re
import natsort
from astropy.io import fits
import numpy as np

def normalize_psf(ipdf,opdf):
    """Normalize the given psf to make the sum of pixels to 1. """

    dat = fits.getdata(ipdf)
    dat /= np.sum(dat) # normalize
    fits.writeto(opdf,dat,overwrite=True)
    
    # checking
    newdat = fits.getdata(opdf)
    mysum = np.sum(newdat)
    print("mysum = {}".format(mysum))


def main():
    """Run main function."""
    for c in list('bdm'):    
        ipdf = 'psf{}_unnorm.fits'.format(c)
        opdf = 'psf{}.fits'.format(c)
        normalize_psf(ipdf,opdf)

if __name__ == "__main__":
    main()
