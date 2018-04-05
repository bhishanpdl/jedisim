#!python
# -*- coding: utf-8 -*-
#
# Author      : Bhishan Poudel; Physics PhD Student, Ohio University
# Date        :  Oct 6, 2017
# Last update :

"""This program creates a text file for weights of bulge and disk narrowbands.

:Depends:  redshift of galaxy and  redshift of cut out galaxies.

:Inputs: The input interpolated sed file to find weights are following:
  sed/ssp_pf_interpolated_z1.5.csv
  sed/exp9_pf_interpolated_z1.5.csv


:Outputs: physics_settings/bd_factors_z1.5.txt # depends on redshift


The weights for bulge and disk narrowbands are calculated using following eqn:

.. math:: b[0] = \\frac{\\int_{\\lambda0}^{\\lambda1} f_b(\\lambda)d\\lambda}{\\int_{\\lambda0}^{\\lambda_{20}} f_b(\\lambda)d\\lambda}

.. math:: d[0] = \\frac{\\int_{\\lambda0}^{\\lambda1} f_d(\\lambda)d\\lambda}{\\int_{\\lambda0}^{\\lambda_{20}} f_d(\\lambda)d\\lambda}

HST ACS FILTERS for F814w:


http://www.stsci.edu/hst/acs/documents/handbooks/current/c05_imaging2.html
Filter Centralwavelength (Å) Width(Å)   Description   Camera
F814W  8333                  2511        Broad I      WFC/HRC

:Command: python a03_scaled_bd_factors.py

:Runtime: 38 seconds.

"""

# Imports
from __future__ import print_function, unicode_literals, division, absolute_import, with_statement
import time, sys, os, argparse
import numpy as np
import scipy as sp
import pandas as pd
from scipy.integrate import simps
import util
from util import updated_config
from astropy.io import fits


def integrate_flux(infile, wav_start, wav_end,column):
    """Integrate the flux between two wavelengths of input sed file."""

    wav,flux_z = np.genfromtxt(infile,usecols=(0,column),unpack=True)
    flx = [flux_z[i] for i in range(len(wav)) if (wav[i] >= wav_start and wav[i] <= wav_end) ]
    integral= simps(flx)

    return integral

def flux_ratio_lsst_hst(sed_b, sed_d, config):
    """Get flux ratio of LSST to HST wavelength ranges.

    sed_b: interpolated file  sed/ssp_pf_interpolated_z1.5.csv
    sed_d: interpolated file sed/exp9_pf_interpolated_z1.5.csv
    config: dictionary from util.updated_config function.

    .. math::

     f_{ratb} = \\frac{\\int_{\\lambda0}^{\\lambda20} f_{bz}(\\lambda)d\\lambda}
     {\\int_{\\lambda{hst0}}^{\\lambda_{hst20}} f_{bzcut}(\\lambda)d\\lambda}


     f_{ratd} = \\frac{\\int_{\\lambda0}^{\\lambda20} f_{dz}(\\lambda)d\\lambda}
     {\\int_{\\lambda{hst0}}^{\\lambda_{hst20}} f_{dzcut}(\\lambda)d\\lambda}


    """

    # Wavelengths for LSST r band and HST ACS WFC F814 filter
    lsst_blue  = int(config['LSST_r_blue_wavelength'])         # 5520 Angstrom
    lsst_red   = int(config['LSST_r_red_wavelength'])          # 6910 Angstrom
    hst_center = int(config['HST_ACS_WFC_central_wavelength']) # 8333
    hst_width  = int(config['HST_ACS_WFC_width'])              # 2511

    # redshifts
    z        = float(config['fixed_redshift'])
    z_cutout = float(config['z_cutout'])

    laml0  = lsst_blue / (1 + z)  # 2208.0
    laml20 = lsst_red / (1 + z)  # 2764.0
    lamh0  = ( hst_center - (hst_width/2) ) / (1 + z_cutout) # 7077.5 / 1.2 = 5897.9
    lamh20 = ( hst_center + (hst_width/2) ) / (1 + z_cutout) # 9588.5 / 1.2 = 7990.4

    # Make wavelentghs integer
    # I have interpolated sed wavelenths to the nearest Angstroms.
    laml0  = round(laml0)  # 2208
    laml20 = round(laml20) # 2764
    lamh0  = round(lamh0)  # 5898
    lamh20 = round(lamh20) # 7990

    # lsst integrals for bulge and disk (column 1 is galaxy age for redshift z)
    int_lsst_bz    = integrate_flux(sed_b, laml0, laml20, 1)
    int_lsst_dz    = integrate_flux(sed_d, laml0, laml20, 1)

    # hst integrals for bulge and disk for z cutout (column 2 is hst galaxy age 12 Gyr)
    int_hst_bzcut  = integrate_flux(sed_b, lamh0, lamh20, 2)
    int_hst_dzcut  = integrate_flux(sed_d, lamh0, lamh20, 2)



    # Flux ratios
    f_ratb = int_lsst_bz / int_hst_bzcut
    f_ratd = int_lsst_dz / int_hst_dzcut

    # Return Value
    return f_ratb, f_ratd

def sum_of_all_pixels_bdh(file_bulge, file_disk):
    datb = fits.getdata(file_bulge)
    datd = fits.getdata(file_disk)

    fluxb = np.sum(datb)
    fluxd = np.sum(datd)
    fluxh = fluxb + fluxd


    # print("np.sum(datb) = {}".format(np.sum(datb)))

    return fluxb, fluxd, fluxh


def flux_bdh_201(config):
    NUM_GAL = int(config['num_source_images']) # 201
    F_b, F_d, F_h = [], [], []

    for n in range(NUM_GAL):
        file_bulge = 'simdatabase/bulge_f8/f814w_bulge{:d}.fits'.format(n)
        file_disk = 'simdatabase/disk_f8/f814w_disk{:d}.fits'.format(n)

        fluxb, fluxd, fluxh = sum_of_all_pixels_bdh(file_bulge, file_disk)
        F_b.append(fluxb)
        F_d.append(fluxd)
        F_h.append(fluxh)

    # make 2d numpy array column vectors
    F_b = np.array(F_b)[None].T
    F_d = np.array(F_d)[None].T
    F_h = np.array(F_h)[None].T

    return F_b, F_d, F_h

def bf_df(sed_b, sed_d, config):
    """Write the file physics_settings/bd_factors.txt."""

    F_b, F_d, F_h = flux_bdh_201(config)
    f_ratb, f_ratd = flux_ratio_lsst_hst(sed_b, sed_d, config)


    F_hstscale = F_b * f_ratb + F_d * f_ratd
    F_cor = F_h / F_hstscale

    bf = F_cor * f_ratb
    df = F_cor * f_ratd

    ofile = config['bd_factors']
    np.savetxt(ofile,np.c_[bf,df],fmt=str('%.14f'))

    # print("f_ratb, f_ratd = {:.3f}, {:.3f}".format(f_ratb, f_ratd))
    # print("F_b.T          = {}".format(F_b.T))
    # print("F_hstscale.T   = {}".format(F_hstscale.T))
    # print("F_cor.T        = {}".format(F_cor.T))
    # print("bf.T           = {}".format(bf.T))
    # print("df.T           = {}".format(df.T))

def main():
    # Usage: python a3_bd_weights.py -z 1.5
    # Runtime: 1.6 sec

    # Config parameters
    config = updated_config('physics_settings/configb.sh')
    z = float(config['fixed_redshift'])

    # Variables
    sed_b = 'sed/ssp_pf_interpolated_z{}.csv'.format(z)
    sed_d = 'sed/exp9_pf_interpolated_z{}.csv'.format(z)

    file_bulge = 'sed/ssp_pf_interpolated_z{}.csv'.format(z)
    file_disk = 'sed/exp9_pf_interpolated_z{}.csv'.format(z)


    # Run the main program
    bf_df(sed_b, sed_d, config)



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
