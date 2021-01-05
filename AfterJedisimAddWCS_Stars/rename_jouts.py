#!python
# -*- coding: utf-8 -*-#
"""
Rename jedisim output files

Author : Bhishan Poudel
Date   : May 7, 2018

"""
# Imports
import os
import glob
import re

# NOTE: comment line36  and line 45 for os.rename for next time.
#
# Rename filenames
def rename_files(idir,z,start,end,increment):
    """ Rename all files in a folder.

    Examples:
    idir = pisces_z1.5_11_15
    start  = 11
    end  = 15
    increment = 10 # this will give 21 to 25
    """
    folders_txt = ['catalog','catalog90','dislist','dislist90']
    folders_fits = ['lsst','lsst90','lsst_mono','lsst_mono90']

    for folder in folders_txt:
        for i in range(start,end+1):
            # try/catalog/catalog_z1.5_000.txt
            f  = '{}/{}/{}_z{:.1f}_{:03d}.txt'.format(idir,folder,folder,z,i)
            f2 = '{}/{}/{}_z{:.1f}_{:03d}.txt'.format(idir,folder,folder,z,i+increment)
            print("\n")
            print('From: ', f)
            print('To  : ', f2)
            #os.rename(f, f2)

    for folder in folders_fits:
        for i in range(start,end+1):
            # try/lsst/lsst_z1.5_000.fits
            f  = '{}/{}/{}_z{:.1f}_{:03d}.fits'.format(idir,folder,folder,z,i)
            f2 = '{}/{}/{}_z{:.1f}_{:03d}.fits'.format(idir,folder,folder,z,i+increment)
            print("\n")
            print('From: ', f)
            print('To  : ', f2)
            #os.rename(f, f2)


def main():
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument('-idir','--idir',required=True,type=str)
    parser.add_argument('-z','--redshift',required=True,type=float)
    parser.add_argument('-s','--start',required=True,type=int)
    parser.add_argument('-e','--end',required=True,type=int)
    parser.add_argument('-new','--new',required=True,type=int,help='the new number we want to start from')

    args  = parser.parse_args() # longer names will be parsed
    idir  = args.idir
    z     = args.redshift
    start = args.start
    end   = args.end
    new   = args.new

    increment = new - start
    rename_files(idir,z,start,end,increment)
    #
    # NOTE: once used this script, comment two os.rename for future.
if __name__ == '__main__':
    main()


# command
# python rename_jouts -idir try -z 1.5 -s 0 -e 2 -new 512
