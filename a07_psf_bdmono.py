#!python
# -*- coding: utf-8 -*-#
###########################################################################
# Author      : Bhishan Poudel; Physics Graduate Student, Ohio University
# Date        : Sep 18, 2017
# Last update :
###########################################################################
"""
:Topic: Create weighted PSF for bulge, disk and monochromatic images.

Weighted psf for bulge is created from sum of all the 21 psfs divided by
sum of 21 bulge weights.

Weighted psf for disk is created from sum of all the 21 psfs divided by
sum of 21 disk weights.

Weighted psf for monochromatic image is created from summing weighted_bulge_scaled
and weighted_disk_scaled. I.e. we first multiply weighted_bulge with frb and weightes_disk
with frd then add them together.

fr is given by (sum_fsb / sum_fsd) / NUM_GALS.
frd is (1/1+fr)  and frb is 1 - frd.

:Outputs: psf/psfb.fits, psfd.fits, and psfm.fits

:Command: python a07_psf_bdmono.py

:Runtime: 10 sec (Oct 18, 2017 Pisces)

"""
# Imports
from __future__ import print_function, unicode_literals, division, absolute_import, with_statement
import time, os, sys, shutil, argparse
from astropy.io import fits
import numpy as np
from util import updated_config, get_bulge_disk_weights


def create_psfbd(b_or_d, ofits):
    """Create PSF for bulge or disk images.

    Args:

      b_or_d (array): array of bulge or disk weights.

      ofits(str): output name of fitsfiles.

    """
    print('Creating: ', ofits)

    # get the shape of input data and create null fits
    dat0 = fits.getdata('psf/psf0.fits').astype(np.float64)
    dat = np.zeros(dat0.shape)

    # add data
    for i in range(0,21):
        # print('i = {}, b[i] = {}'.format(i,b_or_d[i]))
        dat += fits.getdata('psf/psf{:d}.fits'.format(i)).astype(np.float64) * b_or_d[i]

    # average the dat
    dat = dat / np.sum(b_or_d)
    dat /= np.sum(dat) # normalize

    # write fitsfile
    hdu = fits.PrimaryHDU(dat)
    hdu.writeto(ofits,clobber=True)

def create_psfmono(frb, frd, psfb, psfd, ofits):
    """Create PSF for monochromatic image.

    Note that we calculate scaled bulge disk fraction using the formula

      :math:`f_r = \\frac{\\sum  \\frac{f_{sb}}{f_{sd}}}{n_g}`.

    Args:

      frb (float): Fraction ratio value for bulge. :math:`f_{rb} = \\frac{f_r}{1 + f_r}`
      frd (float): Fraction ratio value for disk. :math:`f_{rd} = \\frac{1}{1 + f_r}`
      psfb (str): Input weighted PSF for bulge.
      psfd (str): Input weighted PSF for disk.
      ofits (str): Output fitsfile name for psf monochormatic.

    For 201 f814w base galaxies and for redshift 1.5.
    We have following numbers.

      :math:`fr = 0.0050 frd = 0.9950 frb = 4.9504e-03`  # for z = 1.5

    """
    print('Creating: ', ofits)

    # Make the numbers float
    frd, frb = float(frd), float(frb)


    # get data
    datb = fits.getdata(psfb).astype(np.float64)
    datd = fits.getdata(psfd).astype(np.float64)

    # do the caluculation
    dat = datb * frb + datd * frd
    dat /= np.sum(dat) # normalize

    # write fitsfile
    hdu = fits.PrimaryHDU(dat)
    hdu.writeto(ofits,clobber=True)

def main():
    """Run main function."""
    # Runtime: 8 sec

    # get file path
    config_path = 'physics_settings/configb.sh'
    config = updated_config(config_path)
    bd_flux_rat = config['bd_flux_rat']
    print("bd_flux_rat = {}".format(bd_flux_rat))

    # get two scalar values: scaled_bulge_ratio and  scaled_disk_ratio
    frb, frd = np.genfromtxt(bd_flux_rat, unpack=True, dtype=float)
    print("frb = {}, frd = {}".format(frb, frd))


    # get bulge and disk weights
    b, d = get_bulge_disk_weights(config_path)

    # get psf path names for weighted psf files to be written.
    psfb, psfd, psfm = config['psfb'], config['psfd'], config['psfm']

    # create bulge and disk psf
    create_psfbd(b,psfb)
    create_psfbd(d, psfd)

    # create monochromatic psf
    create_psfmono(frb, frd, psfb, psfd, psfm)


##==============================================================================
## Main program
##==============================================================================
if __name__ == '__main__':

    # beginning time
    begin_time,begin_ctime = time.time(), time.ctime()

    # run main program
    main()

    # print the time taken
    end_time,end_ctime  = time.time(), time.ctime()
    seconds             = end_time - begin_time
    m, s                = divmod(seconds, 60)
    h, m                = divmod(m, 60)
    d, h                = divmod(h, 24)
    print('\nBegin time: ', begin_ctime,'\nEnd   time: ', end_ctime,'\n' )
    print("Time taken: {0:.0f} days, {1:.0f} hours, \
          {2:.0f} minutes, {3:f} seconds.".format(d, h, m, s))
    print("End of Program: {}".format(os.path.basename(__file__)))
    print("\n")
