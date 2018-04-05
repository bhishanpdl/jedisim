#!python
# -*- coding: utf-8 -*-
""" This program creates 3 catalog files viz. catalog, convolvedlist and distortedlist.

The program jedicatalog creates 3 catalog files viz. catalog, convolvedlist
and distortedlist.  This program runs jedicatalog for the bulge and gets
3 catalog files. Then it will copy these three catalogs changing output folder
names and keeping all the other physics parameters same. For example,
position,angle,magnitude,radius of the galaxies are kept same for bulge0.fits,
disk0.fits, and bulge_disk0.fits.


The program jedicatalog will read 201 scaled_bulge, or scaled_disk,
or scaled_bulge_disk galaxies according to config.sh files and from these
fitsfiles it will read the four headers MAG, MAG0, PIXSCALE, RADIUS to
create realistic catalog of galaxies.

:Depends: The program jedicatalog will depend on following:
  - physics_settings/configb.sh or configd.sh or configm.sh
  - simdatabase/scaled_bulge_f8/f814w_scaled_bulge0.fits to 200.fits
  - simdatabase/scaled_disk_f8/f814w_scaled_disk0.fits to 200.fits
  - simdatabase/scaled_bulge_disk_f8/f814w_scaled_bulge_disk0.fits to 200.fits

:Outputs: The output catalog files are following:

  - jedisim_out/out0/trial1_catalog.txt
  - jedisim_out/out90/trial1_catalog.txt

  - jedisim_out/out0/trial1_convolvedlist.tx
  - jedisim_out/out90/trial1_convolvedlist.txt

  - jedisim_out/out0/trial1_distortedlist.txt
  - jedisim_out/out90/trial1_distortedlist.txt

  Jeidcatalog will create three catalogs and this program will rotate them.

:Runtime: 30 seconds (July 27, 2017 Pisces)

"""
# Import
from __future__ import print_function, unicode_literals, division, absolute_import, with_statement
from util import replace_outfolder, run_process, updated_config, get_bulge_disk_weights
import time, os, sys, shutil, argparse
import numpy as np
import time
import re

def run_jedicatalog(config_path):
    # Make the catalog of galaxies (three text files)
    run_process("jedicatalog", ["./executables/jedicatalog",
        config_path])

def rotate_outfolder_angle_catalog(config):
    """Update the output folder name and rotate angle by 90 degree for catalog.txt.

    Changes ::

      jedisim_out/out0/trial1_catalog.txt
      jedisim_out/out90/trial1_catalog.txt

      name                                              x           y
      simdatabase/bulge_disk_f8/bdf8_255.fits	3165.936523	4969.229004


      angle         redshift    pixscale    old_mag     old_rad     new_mag
      332.907227	1.500000	0.060000	24.766600	0.232020	25.990000

      new_rad   stamp_name
      0.176100	jedisim_out/out0/transformed_12/transformed_12419.fits.gz


      dis_name
      jedisim_out/out0/distorted_12/distorted_12419.fits


      For 90 degree roatated case, out0 will be out90 and angle will be
      332.907227 + 90 = 422.907227 - 360 = 62.907227

    """
    ifile = config['catalog_file']
    ofile = config['90_catalog_file']
    old_catalog_file = open(ifile, 'r')
    catalog_file = open(ofile, 'w')
    angle0, angle90 = 0, 0
    for old_line in old_catalog_file:
        l = old_line.split("\t")
        angle0 = float(l[3])
        angle90 = angle0 + 90
        if angle90 >= 360:
            angle90 -= 360
        l[3] = str(angle90)
        l[-1] = l[-1].replace(config['output_folder'], config['90_output_folder'])
        l[-2] = l[-2].replace(config['output_folder'], config['90_output_folder'])
        line = "\t".join(l)
        catalog_file.write(line)

    old_catalog_file.close()
    catalog_file.close()


def rotate_outfolder_convolvedlist(config):
    """Update the output folder name in convolvedlist.txt.

    Changes ::

      jedisim_out/out0/trial1_convolvedlist.txt
      jedisim_out/out90/trial1_convolvedlist.txt

      jedisim_out/out0/convolved/convolved_band_0.fits
      jedisim_out/out90/convolved/convolved_band_0.fits

    """
    old_convolvedlist_file = open(config['convolvedlist_file'], 'r')
    convolvedlist_file = open(config['90_convolvedlist_file'], 'w')
    for old_line in old_convolvedlist_file:
        line = old_line.replace(config['output_folder'],
                                config['90_output_folder'])
        convolvedlist_file.write(line)
    old_convolvedlist_file.close()
    convolvedlist_file.close()


def rotate_outfolder_distortedlist(config):
    """Update the output folder name in distortedlist.txt.

    Changes ::

      jedisim_out/out0/scaled_bulge/trial1_distortedlist.txt
      jedisim_out/out90/scaled_bulge/trial1_distortedlist.txt

      jedisim_out/out0/scaled_bulge/distorted_0/distorted_0.fits
      jedisim_out/out90/scaled_bulge/distorted_0/distorted_0.fits

    """
    old_distortedlist_file = open(config['distortedlist_file'], 'r')
    distortedlist_file = open(config['90_distortedlist_file'], 'w')
    for old_line in old_distortedlist_file:
        line = old_line.replace(config['output_folder'],
                                config['90_output_folder'])
        distortedlist_file.write(line)
    old_distortedlist_file.close()
    distortedlist_file.close()


def jedisim_3cats():
    """Run main function."""
    # Create catalogs
    config_paths = ['physics_settings/config{}.sh'.format(c) for c in list('bdm') ]

    # First create 3 catalogs for bulge (catalog,convolvedlist,distortedlist)
    # Then, copy these files with changed output folders keeping physics
    # parameters same.
    run_jedicatalog(config_paths[0])

    # create catalog.txt for disk and bulge_disk
    with open('jedisim_out/out0/scaled_bulge/trial1_catalog.txt') as fi,\
        open('jedisim_out/out0/scaled_disk/trial1_catalog.txt','w') as fo1,\
        open('jedisim_out/out0/scaled_bulge_disk/trial1_catalog.txt','w') as fo2:

        for line in fi.readlines():
            fo1.write(line.replace('bulge','disk'))
            fo2.write(line.replace('bulge','bulge_disk'))

    # create convolvedlist.txt for disk and bulge_disk
    with open('jedisim_out/out0/scaled_bulge/trial1_convolvedlist.txt') as fi,\
        open('jedisim_out/out0/scaled_disk/trial1_convolvedlist.txt','w') as fo1,\
        open('jedisim_out/out0/scaled_bulge_disk/trial1_convolvedlist.txt','w') as fo2:

        for line in fi.readlines():
            fo1.write(line.replace('bulge','disk'))
            fo2.write(line.replace('bulge','bulge_disk'))

    # create distortedlist.txt for disk and bulge_disk
    with open('jedisim_out/out0/scaled_bulge/trial1_distortedlist.txt') as fi,\
        open('jedisim_out/out0/scaled_disk/trial1_distortedlist.txt','w') as fo1,\
        open('jedisim_out/out0/scaled_bulge_disk/trial1_distortedlist.txt','w') as fo2:

        for line in fi.readlines():
            fo1.write(line.replace('bulge','disk'))
            fo2.write(line.replace('bulge','bulge_disk'))

    ## Copy three catalogs to 90 degree rotated folder.
    for config_path in config_paths:
        config = updated_config(config_path)
        rotate_outfolder_angle_catalog(config)
        rotate_outfolder_convolvedlist(config)
        rotate_outfolder_distortedlist(config)

def main():
    jedisim_3cats()


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
