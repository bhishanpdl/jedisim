#!python
# -*- coding: utf-8 -*-#
#
# Author      : Bhishan Poudel; Physics Graduate Student, Ohio University
# Date        : July 26, 2017
# Last update : Nov 03, 2020

'''

This program adds the PSF stars to all the lsst, lsst90, lsst_mono and lsst_mono90 fitsfiles from the PSF files from another directory (e.g. stars_z1.5_400_e3_e7)

This program does not create star files, it just combines stars to the jedisim output galaxies.

# Note: 1. idir must have lsst,lsst90,lsst_mono and lsst_mono90 dir.
#       2.  stars_z{z}_{nstar}_{low}_{high}/star{b,d,m}_z{z}_{nstar}_{low}_{high}.fits
#           stars_z1.5_400_e3_e7/starb_z1.5_400_e3_e7.fits
#
#                                 z   idir          nstar low high
# Command: python add_wcs_star.py 1.5 files_000_099 400 e3 e7
#
# Outputs: wcs_star_$idir   with star and wcs added to input fitsfiles.

'''


#
# Imports
from __future__ import print_function, unicode_literals, division, absolute_import, with_statement
from astropy.cosmology import FlatLambdaCDM
import glob
import os
import numpy as np
from astropy.io import fits
from astropy import wcs
import sys

def add_wcs(field):
    # Read field
    field = str(field)
    field_hdu = fits.open(field)

    # Get fake wcs from astropy
    w = wcs.WCS(naxis=2)
    w.wcs.crpix = [1800.0, 1800.0]
    w.wcs.crval = [0.1, 0.1]
    w.wcs.cdelt = np.array([-5.55555555555556E-05,5.55555555555556E-05])
    w.wcs.ctype = ["RA---TAN", "DEC--TAN"]
    wcs_hdr = w.to_header()

    # Add fake wcs to header of output file
    hdr = field_hdu[0].header
    hdr += wcs_hdr

    # Write output file
    field_hdu.writeto(field,clobber=True)
    field_hdu.close()

    # Print
    print('Fake WCS added to the galaxy field: {}'.format(field))

def main():
    """Run main function."""
    z = sys.argv[1] # 1.5
    idir = sys.argv[2]  # jout_z0.5_000_099 (inside this
                        #   we must have lsst, lsst_mono and 90s.
    idir = idir.rstrip('/') # jout_00/ ==> jout_00

    nstar = sys.argv[3]
    low = sys.argv[4] # e3
    high = sys.argv[5] # e7

    mono = ['lsst_mono','lsst_mono90']
    chro = ['lsst','lsst90']

    mono = ['{}/{}/'.format(idir,f) for f in mono]
    chro = ['{}/{}/'.format(idir,f) for f in chro]

    # star data
    # stars_z1.5_400_e3_e7/starb_z1.5_400_e3_e7.fits
    dat_stars = [fits.getdata('stars_z{}_{}_{}_{}/star{}_z{}_{}_{}_{}.fits'.format(
        z,nstar,low,high,i,z,nstar,low,high)) for i in list('bdm')]

    # create output dirs
    odirs = ['wcs_star_{}'.format(o) for o in mono+chro]
    for o in odirs:
        if not os.path.isdir(o):
            os.makedirs(o)

    # mono
    for m in mono:
        for f in glob.glob('{}/*.fits'.format(m)):
            datm = fits.getdata(f)
            odat = datm + dat_stars[2] # mono + starm
            head, tail = os.path.split(f)
            ofile = 'wcs_star_' + head + '/' + tail
            print('\nWriting: ', ofile)
            fits.writeto(ofile,odat,clobber=True)
            add_wcs(ofile)

    # chro
    for c in chro:
        for f in glob.glob('{}/*.fits'.format(c)):
            datc = fits.getdata(f)
            odat = datc + dat_stars[0] + dat_stars[1] # chro + starb + stard
            head, tail = os.path.split(f)
            ofile = 'wcs_star_' + head + '/' + tail
            print('\nWriting: ', ofile)
            fits.writeto(ofile,odat,clobber=True)
            add_wcs(ofile)

if __name__ == "__main__":
    main()

# Note: 1. idir must have lsst,lsst90,lsst_mono and lsst_mono90 dir.
#       2.  stars_z{z}_{nstar}_{low}_{high}/star{b,d,m}_z{z}_{nstar}_{low}_{high}.fits
#
#                                 z   idir            nstar low high
# Command: python add_wcs_star.py 1.5 files_000_099 300 e3 e7
# Command: python add_wcs_star.py 1.5 files_000_099/ 300 e3 e7 # the last / of folder name will be stripped
#
# Outputs: wcs_star_$idir   with star and wcs added to input fitsfiles.
# Run time:

