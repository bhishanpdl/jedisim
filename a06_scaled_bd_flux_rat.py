#!python
# -*- coding: utf-8 -*-#
###########################################################################
# Author      : Bhishan Poudel; Physics Graduate Student, Ohio University
# Date        : Sep 18, 2017
# Last update :
###########################################################################
"""
Get flux ratio of scaled bulge and scaled disks.

:Inputs: This programa reads all the 201 scaled bulge and scaled disk images.

:Output: After summing all the fluxes we get fraction ratios as follows

  :math:`f_r = \\frac{\\sum  \\frac{f_{sb}}{f_{sd}}}    {n_g}`

  :math:`f_{rd} = \\frac{1}{1 + f_r}`

  :math:`f_{rb} = \\frac{f_r}{1 + f_r}`

  :math:`fr = 0.0022 frb = 0.0021 frd = 0.99785444`  # for z = 1.5

.. note::

   Note that these bulge and disk fractions depend on the redshift since
   while creating scaled bulge and scaled disk we had used redshift
   dependent weights.

:Command: python a06_scaled_bd_flux_rat.py
:Runtime: 28 secs.

"""
# Imports
from __future__ import print_function, unicode_literals, division, absolute_import, with_statement
import time
import os
import numpy as np
from astropy.io import fits
from util import updated_config


# Global variable
NUM_GALS = 201


def sbd_flux_ratio(ofile):
    mysum_sb, mysum_sd = 0.0, 0.0
    for i in range(NUM_GALS):

        # for scaled bulge
        infile_sb = 'simdatabase/scaled_bulge_f8/f814w_scaled_bulge{:d}.fits'.format(i)
        dat_sb = fits.getdata(infile_sb)
        sum_sb = np.sum(np.array(dat_sb))
        mysum_sb += sum_sb

        # for scaled disk
        infile_sd = 'simdatabase/scaled_disk_f8/f814w_scaled_disk{:d}.fits'.format(i)
        dat_sd = fits.getdata(infile_sd)
        sum_sd = np.sum(np.array(dat_sd))
        mysum_sd += sum_sd

        # debug
        # print("sum_sb = {}".format(sum_sb))
        # print("mysum_sb = {}".format(mysum_sb))

    # debug
    # print("mysum_sb = {}".format(mysum_sb))
    # print("mysum_sd = {}".format(mysum_sd))

    # now get ratio
    fr = mysum_sb / mysum_sd / NUM_GALS
    frd = 1 / ( 1 + fr)
    frb = 1 -frd

    # Write to a textfile, calling this function takes 20 secs.
    with open(ofile,'w') as fo:
        fo.write("# fr = (sum_Fsb/sum_Fsd) / NUM_GALS  where Fsb is sum of fluxes of 201 scaled bulge galaxies.\n")
        fo.write("# frb = fr/ (1+fr)\n")
        fo.write("# frd = 1 / (1 + fr)\n")
        fo.write("# frb                frd   \n")
        line = str(frb) + '    ' +  str(frd) + '\n'
        fo.write(line)

    return fr, frb, frd

def main():
    """Run main function."""
    # Get file name to write output
    # ofile = 'physics_settings/bd_flux_rat_z1.5.txt'
    config_path = 'physics_settings/configb.sh'
    config = updated_config(config_path)
    ofile = config['bd_flux_rat']
    print("Creating: {}".format(ofile))

    # Now run the main program
    fr, frb, frd = sbd_flux_ratio(ofile)

    # Print output values
    print("fr = {:.4f} frb = {:.4f} frd = {:.8f}".format(fr, frb, frd))


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
