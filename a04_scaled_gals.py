#!python
# -*- coding: utf-8 -*-
#
###########################################################################
# Author      : Bhishan Poudel; Physics Graduate Student, Ohio University
# Date        : Jun 10, 2017 Sat
# Last update :
###########################################################################
"""
Generate scaled_bulge, scaled_disk, and scaled_mono galaxies.

:Info: This program will read the bulge and disk factor columns from
  the text file `physics_settings/bd_factors.txt`, and then use these
  numbers to create scaled_bulge, scaled_disk, and scaled_bulge_disk files.

:Inputs:

  simdatabase/bulge_f8/f814w_bulge0.fits to 200.fits
  simdatabase/disk_f8/f814w_disk0.fits to 200.fits

:Outputs:

  simdatabase/scaled_bulge_f8/f814w_scaled_bulge0.fits to 200.fits
  simdatabase/scaled_disk_f8/f814w_scaled_disk0.fits to 200.fits
  simdatabase/scaled_bulge_disk_f8/f814w_scaled_bulge_disk0.fits to 200.fits

.. note::

   The follow up program `jedicatalog` will need the header keys
   MAG, MAG0, PIXSCALE, and RADIUS so, we need at least these header
   keywords in all of the output fitsfiles.

:Command: python a04_scaled_gals.py

:Runtime: 1 minutes, 30 seconds. (Oct 2, 2017 Pisces)

"""
# Imports
from __future__ import print_function, unicode_literals, division, absolute_import, with_statement
import time, sys, os, shutil,argparse
from astropy.io import fits
from astropy.io.fits import getdata, getheader
import numpy as np
from util import updated_config, replace_outfolder

# Global variable
NUM_GALS = 201


def scale_galaxies(NUM_GALS, config):
    # first get bulge disk factors
    # The function get_bulge_disk gets names of input
    # file for bulge_disk weights from config path.
    # e.g.
    # bd_factors="physics_settings/bd_factors.txt"
    bd_factors = config['bd_factors']
    b, d = np.genfromtxt(bd_factors, usecols=(0,1),dtype=float,unpack=True)

    for i in range(NUM_GALS):
        # for bulge

        # Bulge
        infileb = 'simdatabase/bulge_f8/f814w_bulge{:d}.fits'.format(i)
        outfileb = 'simdatabase/scaled_bulge_f8/f814w_scaled_bulge{:d}.fits'.format(i)
        datb = fits.getdata(infileb)
        datb = datb * b[i]
        fits.writeto(outfileb, datb, header = getheader(infileb), clobber=False)

        # for disk
        infiled = 'simdatabase/disk_f8/f814w_disk{:d}.fits'.format(i)
        outfiled = 'simdatabase/scaled_disk_f8/f814w_scaled_disk{:d}.fits'.format(i)
        datd = fits.getdata(infiled)
        datd = datd * d[i]
        fits.writeto(outfiled, datd, header = getheader(infiled), clobber=False)

        # for monochromatic we combine them
        outfile = 'simdatabase/scaled_bulge_disk_f8/f814w_scaled_bulge_disk{:d}.fits'.format(i)
        dat = datb + datd
        fits.writeto(outfile, dat, header = getheader(infiled), clobber=False)


def main():
    """Run main function."""
    # Runtime: 1 min 30 sec
    config_path = 'physics_settings/configb.sh'
    config = updated_config(config_path)

    # Create output dirs
    replace_outfolder('simdatabase/scaled_bulge_f8')
    replace_outfolder('simdatabase/scaled_disk_f8')
    replace_outfolder('simdatabase/scaled_bulge_disk_f8')

    # Now write files into them.
    scale_galaxies(NUM_GALS, config)

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
