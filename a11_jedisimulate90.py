#!python
# -*- coding: utf-8 -*-
"""This program makes a realistic simulation of LSST images.

.. note:: TDCR is transform-distort-convolve-rescale:

  - jeditransform will transforms bulge-disk fitsfiles and creates 12420 zipped stamps and also create dislist.txt.
  - jedidistort will distort the zipped stamps according to the dislist.txt and writes 12420 unzipped distorted fitsfiles.
  - jedipaste will combine these 12420 distorted images into one large HST.fits according to distortedlist.txt.
  - jediconvolve will convolve HST.fits with psfb.fits or psfd.fits or psfm.fits and creates 6 convolved bands.
  - jedipaste will combine these 6 convolved bands and create HST_convolved_image.
  - jedirescale will scale down this HST_convolved_image to lsst_bulge.fits and so on.

:Runtime:

  21 minutes for 201 base galaxies. (Oct 2, 2017 Pisces)

"""
# Imports
from __future__ import print_function, unicode_literals, division, absolute_import,with_statement
import os
import sys
import subprocess
import math
import re
import shutil
import copy
import time
import numpy as np
from astropy.io import fits
# local imports
from util import replace_outfolder, run_process, updated_config, add_stars, add_wcs

# NOTE: for 90 degree odirs and catalogs are already created.

def lsst_TDCR(config, psf_name, rescaled_outfile90,multiply_value):
    """Create a single lsst_bulge or lsst_disk or lsst_bulge_disk image
    images after running 6 programs. We will add noise to this later.

    Args:
      config_path (str): input physics config file.
        e.g. physics_settings/configb.sh
        e.g. physics_settings/configd.sh

      psf_names (str): input psf file for scaled_bulge or unscaled_disk
        e.g. config['psfb'] = psf/psfb.fits
        e.g. config['psfd'] = psf/psfd.fits

      rescaled_outfile (str): output after running 6 programs.
        This is the final output of program jedirescale.
        e.g. config['rescaled_outfileb'] = lsst_bulge.fits
        e.g. config['rescaled_outfiled'] = lsst_disk.fits
        e.g. config['rescaled_outfilebd'] = lsst_bulge_disk.fits

    :Outputs: The outputs are following:

      jedisim_out/out0/lsst_bulge.fits
      jedisim_out/out0/lsst_disk.fits
      jedisim_out/out0/lsst_bulge_disk.fits

    Note that we combine these two files and call it chromatic lsst.fits.
    We convolve this image with monochromatic psf and call that lsst_mono.fits.

    The keys that has 90 prefix on them are following ::

          keys = ['catalog_file',         'dislist_file',
                  'distortedlist_file',   'convolvedlist_file',
                  'HST_image',            'HST_convolved_image',
                  'rescaled_outfileb',    'rescaled_outfiled',
                  'rescaled_outfilem',    'lsst_unnoised',
                  'lsst',                 'lsst_mono' ]

    :Runtime: 5 min 44 sec for 201 scaled bulge galaxies.

    """
    # Transform scaled_bulge or scaled_disk fitsfiles according to:
    # jedisim_out/out0/scaled_bulge/trial1_catalog.txt.
    #
    # jeditransform will create 12420 .gz fitsfiles. For example:
    # jedisim_out/out0/scaled_bulge/transformed_0/transformed_0_to_999.fits.gz  (for stamps 0 to 12 )
    #
    # It also creates dislist for the jedidistort,viz.,
    # jedisim_out/out0/scaled_bulge/trial1_dislist.txt
    run_process("jeditransform", ['./executables/jeditransform',
                                  config['90_catalog_file'],
                                  config['90_dislist_file']
                                  ])

    # This program distorts the 12420 galaxies from jedisim_out/out0/transformed_/
    # according to dislist.txt and lens.txt and write distorted
    # galaxies inside 13 folders jedisim_out/out0/distorted_/
    #
    # In the end we get unzipped distorted images in 13 folders.
    # jedisim_out/out0/distorted_0/distorted_0.fits 1000*12+ 420 fitsfiles.
    run_process("jedidistort", ['./executables/jedidistort',
                                config['nx'],
                                config['ny'],
                                config['90_dislist_file'],
                                config['lens_file'],
                                config['pix_scale'],
                                config['lens_z']
                                ])

    # This program combines 12,420 distorted fits files inside the
    # jedisim_out/out0/distorted_/distorted_fits/
    # into a single large embedded image: jedisim_out/out0/HST.fits.
    run_process("jedipaste", ['./executables/jedipaste',
                              config['nx'],
                              config['ny'],
                              config['90_distortedlist_file'],
                              config['90_HST_image']
                              ])
    #
    # XXX: Added  Mar 26, 2018
    # multiply_value = 1 for monochromatic
    # multiply_value = fb = 0.00143809456161  for z = 0.7
    # multiply_value = fd = 0.998561905438    for z = 0.7
    #  ---------------------------------------------------
    #    sum of fr and fb = 1.0
    #
    # fb is for bulge, and fd is for disk
    data = fits.getdata(config['90_HST_image']) * float(multiply_value)
    fits.writeto(config['90_HST_image'],data,clobber=True)


    # XXX: ADDED  Mar 25, 2018
    add_stars(config['90_HST_image'], config['n_stars'], config['star_value'],config['star_positions'])
    
    # Convolve the given single fitsfile with given PSF and write 6 bands
    # of convolved images.
    # E.g. convolve HST.fits with psfb.fits to get 6 bands of convolved images.
    run_process("jediconvolve", ['./executables/jediconvolve',
                                 config['90_HST_image'],
                                 psf_name,
                                 config['90_output_folder'] + 'convolved/'
                                 ])

    # Combine 6 convolved bands into one HST_convolved image.
    run_process("jedipaste", ['./executables/jedipaste',
                              config['nx'],
                              config['ny'],
                              config['90_convolvedlist_file'],
                              config['90_HST_convolved_image']
                              ])

    # Change the PIXSCALE of the input fitsfile into another one.
    # e.g. HST has pixscale 0.06 and we change it to LSST pixscale = 0.2
    run_process("jedirescale", ['./executables/jedirescale',
                                config['90_HST_convolved_image'],
                                config['pix_scale'],
                                config['final_pix_scale'],
                                config['x_trim'],
                                config['y_trim'],
                                rescaled_outfile90
                                ])


def lsst_monochromatic(config):
    """Convolve lsst chromatic with psf_mono.fits and get monochromatic image.

    :Output: jedisim_out/out0/lsst_mono.fits

    """
    # Add noise to  monochromatic image and choose this as lsst_mono final output.
    run_process("jedinoise", ['./executables/jedinoise',
                              config['90_rescaled_outfilem'],
                              config['exp_time'],
                              config['noise_mean'],
                              config["90_lsst_mono"]
                              ])
    #
    # XXX: Added  Mar 29, 2018
    # Add fake wcs
    # DMstack obs_file needs WCS info
    add_wcs(config["90_lsst_mono"])

def lsst_chromatic(configb,configd,configm):
    """Combine lsst_bulge and lsst_disk and take this as chromatic.

    :Output: jedisim_out/out0/lsst.fits

    """

    # Combine lsst_bulge with lsst_disk and call it lsst_unnoised.fits
    dat = fits.getdata(configb['90_rescaled_outfileb']) +\
          fits.getdata(configd['90_rescaled_outfiled'])
          
    fits.writeto(configm["90_lsst_unnoised"], dat, 
        header = fits.getheader(configb['90_rescaled_outfileb']),overwrite=True)


    # Add noise to  chromatic image and choose this as lsst final output.
    run_process("jedinoise", ['./executables/jedinoise',
                              configm['90_lsst_unnoised'],
                              configm['exp_time'],
                              configm['noise_mean'],
                              configm["90_lsst"]
                              ])
    #
    # XXX: Added  Mar 26, 2018
    # Add fake wcs
    # DMstack obs_file needs WCS info
    add_wcs(configm["90_lsst"])


def main():
    """Run main function."""

    # Config dictionaries
    configb = updated_config('physics_settings/configb.sh')
    configd = updated_config('physics_settings/configd.sh')
    configm = updated_config('physics_settings/configm.sh')
    # print("configb['90_output_folder'] = {}".format(configb['90_output_folder']))

    # Get factors to multiply bulge and disk
    fb, fd = np.genfromtxt(configm['bd_flux_rat'], dtype=float, unpack=True)

    # Get convolved scaled files g_csb, g_csd , and g_csm
    lsst_TDCR(configb, configb['psfb'], configb['90_rescaled_outfileb'],fb)
    lsst_TDCR(configd, configd['psfd'], configd['90_rescaled_outfiled'],fd)
    lsst_TDCR(configm, configm['psfm'], configm['90_rescaled_outfilem'],1.0)


    # get final monochromatic image
    # jedisim_out/out90/scaled_bulge_disk/trial1_lsst_mono.fits
    lsst_monochromatic(configm)

    # get final chromatic image
    # jedisim_out/out90/scaled_bulge_disk/trial1_lsst.fits
    lsst_chromatic(configb,configd,configm)


if __name__ == "__main__":
    import time

    # Beginning time
    program_begin_time = time.time()
    begin_ctime        = time.ctime()

    #  Run the main program
    main()

    # # Print the time taken
    # program_end_time = time.time()
    # end_ctime        = time.ctime()
    # seconds          = program_end_time - program_begin_time
    # m, s             = divmod(seconds, 60)
    # h, m             = divmod(m, 60)
    # d, h             = divmod(h, 24)
    # print("\nBegin time: ", begin_ctime)
    # print("End   time: ", end_ctime, "\n")
    # print("Time taken: {0: .0f} days, {1: .0f} hours, \
    #   {2: .0f} minutes, {3: f} seconds.".format(d, h, m, s))
