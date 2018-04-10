#!python
# -*- coding: utf-8 -*-
"""
:Author:  Bhishan Poudel; Physics Graduate Student, Ohio University

:Date: Aug 01, 2016

:Last update: Oct 2, 2017

:Inputs:

  1. jedimaster.py, especially the final outputs

:Outputs:
  1. jedisim_output/lsst*.fits
  2. jedisim_output/90_lsst*.fits
  3. jedisim_output/aout10_noise*.fits
  4. jedisim_output/90_aout10_noise*.fits

:Info:
  1. This is a wrapper to run jedisim program and collect it's outputs.
  2. We copy the files from each iteration and name them appropriately.

:Runtime:

:Command: python run_jedisim.py -z 0.7 -c simplici -s 0 -e 0

:Changes:

  - replaced shutil.copyfile by os.rename except for psf copy.
  - Renamed output folder names and dropbox file name.

"""
# Imports
from __future__ import print_function, unicode_literals, division, absolute_import,with_statement
from astropy.cosmology import FlatLambdaCDM
import os
import sys
import subprocess
import math
import re
import shutil
import copy
import time
from util import run_process,updated_config,replace_outfolder,notify

# start time
start_time = time.time()
start_ctime = time.ctime()

def jedisim_outfolders(config_path):
    config = updated_config(config_path)
    jouts = {}
    z = config['fixed_redshift']

    # six galaxies and two texts, total 8*2 output folders.
    # Also there is one output folder for three psfs.
    # So, in total there are 17 output folders.
    # keys = ['lsst', 'lsst_mono', 'gcsb','gcsd','gcsm','catalog','dislist']

    keys = ['lsst', 'lsst_mono', 'catalog','dislist']
    tm   = time.strftime("%Y_%m_%H_%M")
    odirs = ['jedisim_output/jout_z{}_{}/z{}/{}/'.format(z,tm,z,key) for key in keys ]

    for i, odir in enumerate(odirs):
        # replace output dirs
        replace_outfolder(odir)
        replace_outfolder(odir[0:-1]+'90/')

        # also create dictionary along with 90 degree rotated keys
        jouts[keys[i]] = odirs[i]
        jouts[keys[i]+'90'] = odirs[i][0:-1]+'90/'

    # add one psf folder to dictionary jouts
    jouts['psf'] = 'jedisim_output/jout_z{}_{}/z{}/psf'.format(z,tm,z)
    replace_outfolder(jouts['psf'])

    return jouts

# this will run jedisim.py in a loop after creatin jouts (jedisim_output/)
def run_jedisim(start, end, z, computer, config_path,jouts):
    # Write output names in dropbox textfile.
    odir = '/Users/poudel/Dropbox/jout'
    tm = time.strftime("%Y_%m_%d_%H_%M")

    if not os.path.isdir(odir):
        os.makedirs(odir)
    otxt =  '{}/jout_{}_z{}_{}.txt'.format(odir,computer,z,tm)

    # Create empty textfile in dropbox to be added later.
    print('Creating: {}'.format(otxt))
    with open(otxt,'w') as fo:
        fo.write("")


    # before running jedisim, we already have 3 psfs
    # we copy them to appropriate place

    # 1. Copy 3 psf files (bulge,disk,mono for given redshift)
    for p in list('bdm'):
        infile = r'psf/psf{}.fits'.format(p)
        outfile = jouts['psf'] + '/psf{}_z{}.fits'.format(p,z)
        if not os.path.isfile(outfile):
            shutil.copy(infile,outfile)


    # Run jedisim in a loop
    for i in range(start, end+1):

        # Indivisual times
        loop_start_time = time.time()
        print('{} {} {}'.format('Running jedimaster loop :', i, ''))

        run_process("Run jedisim program.", ['python', "jedisim.py"])

        # 1. Copy lsst file
        infile = r'jedisim_out/out0/scaled_bulge_disk/trial1_lsst.fits'
        outfile = jouts['lsst'] + 'lsst_z{}_{}.fits'.format(z,i)
        os.rename(infile, outfile)

        # debug
        # print('From and To for Loop {}: \n{}'.format(i, infile))
        # print('{}\n'.format(outfile))

        # 2. Copy lsst_mono file
        infile = r'jedisim_out/out0/scaled_bulge_disk/trial1_lsst_mono.fits'
        outfile = jouts['lsst_mono'] + 'lsst_mono_z{}_{}.fits'.format(z,i)
        os.rename(infile, outfile)

        # copy gcsb, gcsd, and gcsm only at end of production.
        # # 3. Copy gcsb   convolved-scaled-bulge
        # infile = r'jedisim_out/out0/scaled_bulge/trial1_lsst_bulge.fits'
        # outfile = jouts['gcsb'] + 'gcsb_z{}_{}.fits'.format(z,i)
        # os.rename(infile, outfile)
        #
        #
        # # 4. Copy gcsd convolved-scaled-disk
        # infile = r'jedisim_out/out0/scaled_disk/trial1_lsst_disk.fits'
        # outfile = jouts['gcsd'] + 'gcsd_z{}_{}.fits'.format(z,i)
        # os.rename(infile, outfile)
        #
        #
        # # 5. Copy gcsm convolved-scaled-bulge_disk
        # infile = r'jedisim_out/out0/scaled_bulge_disk/trial1_lsst_bulge_disk.fits'
        # outfile = jouts['gcsm'] + 'gcsm_z{}_{}.fits'.format(z,i)
        # os.rename(infile, outfile)


        # 6. Copy catalog.txt for bulge
        infile = r'jedisim_out/out0/scaled_bulge/trial1_catalog.txt'
        outfile = jouts['catalog'] + 'catalog_z{}_{}.txt'.format(z,i)
        os.rename(infile, outfile)


        # 7. Copy dislist.txt for bulge
        infile = r'jedisim_out/out0/scaled_bulge/trial1_dislist.txt'
        outfile = jouts['dislist'] + 'dislist_z{}_{}.txt'.format(z,i)
        os.rename(infile, outfile)

        ##*************************************************************
        # For 90 degree rotated case
        # 1-90. Copy lsst file
        infile = r'jedisim_out/out90/scaled_bulge_disk/90_trial1_lsst.fits'
        outfile = jouts['lsst90'] + 'lsst90_z{}_{}.fits'.format(z,i)
        os.rename(infile, outfile)

        # 2-90. Copy lsst_mono file
        infile = r'jedisim_out/out90/scaled_bulge_disk/90_trial1_lsst_mono.fits'
        outfile = jouts['lsst_mono90'] + 'lsst_mono90_z{}_{}.fits'.format(z,i)
        os.rename(infile, outfile)

        # NOTE: copy these files only at last step
        # # 3-90. Copy gcsb   convolved-scaled-bulge
        # infile = r'jedisim_out/out90/scaled_bulge/90_trial1_lsst_bulge.fits'
        # outfile = jouts['gcsb90'] + 'gcsb90_z{}_{}.fits'.format(z,i)
        # os.rename(infile, outfile)
        #
        #
        # # 4-90. Copy gcsd convolved-scaled-disk
        # infile = r'jedisim_out/out90/scaled_disk/90_trial1_lsst_disk.fits'
        # outfile = jouts['gcsd90'] + 'gcsd90_z{}_{}.fits'.format(z,i)
        # os.rename(infile, outfile)
        #
        #
        # # 5-90. Copy gcsm convolved-scaled-bulge_disk
        # infile = r'jedisim_out/out90/scaled_bulge_disk/90_trial1_lsst_bulge_disk.fits'
        # outfile = jouts['gcsm90'] + 'gcsm90_z{}_{}.fits'.format(z,i)
        # os.rename(infile, outfile)


        # 6-90. Copy catalog.txt for bulge
        infile = r'jedisim_out/out90/scaled_bulge/90_trial1_catalog.txt'
        outfile = jouts['catalog90'] + 'catalog90_z{}_{}.txt'.format(z,i)
        os.rename(infile, outfile)


        # 7-90. Copy dislist.txt for bulge
        infile = r'jedisim_out/out90/scaled_bulge/90_trial1_dislist.txt'
        outfile = jouts['dislist90'] + 'dislist90_z{}_{}.txt'.format(z,i)
        os.rename(infile, outfile)

        # Append output names in Dropbox
        loop_end_time = time.time()
        loop_time =  loop_end_time - loop_start_time

        loop_mins = loop_time / 60
        date = time.strftime("%b%d %H:%M")
        with open(otxt,'a') as fo:
            fo.write('{} {}: z = {:.1f} Runtime {:.0f} mins and EndDate: {}\n\n'.format(computer, i, z, loop_mins, date))


if __name__ == "__main__":
    # command: python run_jedisim.py 0.7 pisces 0 0

    # Beginning time
    program_begin_time = time.time()
    begin_ctime        = time.ctime()

    # run command:
    # python run_jedisim.py -z 0.7 -c pisces -s 0 -e 0

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--manual", help="python run_jedisim.py -z 0.7 -c simplici -s 0 -e 0 > /dev/null 2>&1 &",type=str, required=False)
    parser.add_argument("-z", "--redshift", help="Redshift of the cluster",type=float, required=True)
    parser.add_argument("-c", "--computer", help="Host computer to running this program.", required=True)
    parser.add_argument("-s", "--start", help="Iteration start",
    		required=True,type=int)
    parser.add_argument("-e", "--end", help="Iteration end",
    		required=True,type=int)
    args = parser.parse_args()
    z = args.redshift
    computer = args.computer
    start = args.start
    end = args.end


    # First create config files configb,configd and configm
    run_process("config", ['python', "a01_jedisim_config.py", "-z %f" % z]) # 0.6 sec

    # Config path (configb is created from template for given redshift.)
    config_path = "physics_settings/configb.sh"

    # Create output folders to copy final files (jedisim_out)
    # after reading configb file.
    jouts = jedisim_outfolders(config_path)


    # Run pre-jedisim programs
    # Takes about 5 mins.
    run_process("interpolate", ['python', "a02_interpolate_sed.py"]) # 3 sec
    run_process("bd factors",  ['python', "a03_scaled_bd_factors.py"]) # 38 sec
    run_process("scaled gals", ['python', "a04_scaled_gals.py"]) # 1.5 min
    run_process("bd weights",  ['python', "a05_bd_weights_psf.py"]) # 3.5 sec
    run_process("bd flux rat", ['python', "a06_scaled_bd_flux_rat.py"]) # 28 sec
    run_process("psf",         ['python', "a07_psf_bdmono.py"]) # 10 sec

    #  Run the main program
    run_jedisim(start, end, z, computer, config_path,jouts)

    # delete temp python directory (unix)
    os.system('rm -rf __pycache__')

    # # notify
    notify()

    # Print the time taken
    program_end_time = time.time()
    end_ctime        = time.ctime()
    seconds          = program_end_time - program_begin_time
    m, s             = divmod(seconds, 60)
    h, m             = divmod(m, 60)
    d, h             = divmod(h, 24)
    print("\n\nBegin time: ", begin_ctime)
    print("End   time: ", end_ctime, "\n")
    print("Time taken: {0: .0f} days, {1: .0f} hours, \
      {2: .0f} minutes, {3: f} seconds.".format(d, h, m, s))

#
"""
:Command: python run_jedisim.py -z 0.7 -c simplici -s 0 -e 0
:Command: python run_jedisim.py -z 0.7 -c simplici -s 0 -e 100 > /dev/null 2>&1
"""
