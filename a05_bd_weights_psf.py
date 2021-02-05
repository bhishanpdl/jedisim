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


:Outputs: physics_settings/bd_weights_z1.5.txt # depends on redshift


The weights for bulge and disk narrowbands are calculated using following eqn:

.. math:: b[0] = \\frac{\\int_{\\lambda0}^{\\lambda1} f_b(\\lambda)d\\lambda}{\\int_{\\lambda0}^{\\lambda_{20}} f_b(\\lambda)d\\lambda}

.. math:: d[0] = \\frac{\\int_{\\lambda0}^{\\lambda1} f_d(\\lambda)d\\lambda}{\\int_{\\lambda0}^{\\lambda_{20}} f_d(\\lambda)d\\lambda}

HST ACS FILTERS for F814w:


http://www.stsci.edu/hst/acs/documents/handbooks/current/c05_imaging2.html
Filter Centralwavelength (Å) Width(Å)   Description   Camera
F814W  8333                  2511        Broad I      WFC/HRC

:Command: python a05_bd_weights_psf.py

:Runtime: 3.5 seconds.

"""

# Imports
from __future__ import print_function, unicode_literals, division, absolute_import, with_statement
import time
import os
import numpy as np
import scipy as sp
import pandas as pd
from scipy.integrate import simps
import util
import sys
import argparse
from util import updated_config

def wavelengths(config):
    """Get lambda_lsst and lambda_hst.

    Here 22 numbers has 21 integral ranges.

    For LSST survey the r-band filter has following parameters:

    Reference: https://www.lsst.org/about/camera/features

    blue side = 552 nm and red side = 691 nm


    The HST survey filter information can be found here:

    http://www.stsci.edu/hst/acs/documents/handbooks/current/c05_imaging2.html

    # These also gives values for filters of HST

    http://svo2.cab.inta-csic.es/svo/theory/fps3/index.php?id=HST/WFPC2.f814w
    http://etc.stsci.edu/etcstatic/users_guide/appendix_b_acs.html

    The wikipedia page about HST survey is here:

    https://en.wikipedia.org/wiki/Hubble_Space_Telescope

    https://en.wikipedia.org/wiki/Advanced_Camera_for_Surveys

    For HST four cameras are active since 2009 (maintainance).

    ACS, COS, STIS, WFC3


    1. Advanced Camera for Surveys (ACS; 2002–present) (3 channels)

        - HRC (disabled)
        - SBC (Solar Blind Channel)
        - WFC (Wide Field Channel)::

            Its detector consists of two butted 2048x4096,
            15 µm/pixel charge-coupled devices (CCDs) for
            a total of 16 megapixels manufactured by Scientific
            Imaging Technologies (SITe). The WFC plate scale
            is 0.05″ per pixel and it has an effective field-of-view of 202″×202″.
            The spectral range of the WFC detector is 350–1100 nm.

    2. Cosmic Origins Spectrograph (COS; 2009–present)
    3. Space Telescope Imaging Spectrograph
       (STIS; 1997–present (non-operative 2004–2009)
    4. Wide Field Camera 3 (WFC3; 2009–present)

      - Wide Field and Planetary Camera (WFPC; 1990–1993)
      - Wide Field and Planetary Camera 2 (WFPC2; 1993–2009)
      - Wide Field Camera 3 (WFC3; 2009–present)

    .. note::

      We are using HST ACS Camera with WFC channel.

    """
    # Wavelength for lsst r band and hst f814 filter
    # The values are for 6 Gyr old galaxy.
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

    # List of 22 values for 21 intervals.
    laml   = np.linspace(start=laml0,stop=laml20,num=22,endpoint=True)
    lamh   = np.linspace(start=lamh0,stop=lamh20,num=22,endpoint=True)

    # Make integers
    laml   = [round(i) for i in laml]
    lamh   = [round(i) for i in lamh]

    # Return Value
    return [laml, lamh]

def integrate_flux(infile, wav_start, wav_end):
    """Integrate the flux between two points of input sed file.

    .. note::

       Sometimes pd.read_csv fails, so use np.genfromtxt to read the datafile.

       In np.genfromtxt dtype is determined indivisually.

       https://docs.scipy.org/doc/numpy/reference/generated/numpy.genfromtxt.html

    """
    wav,flux_z = np.genfromtxt(infile,usecols=(0,1),unpack=True)

    flx = [flux_z[i] for i in range(len(wav)) if (wav[i] >= wav_start and wav[i] <= wav_end) ]

    integral= simps(flx)

    # Return Values
    return integral

def write_bd_weights(config, infileb, infiled,outfile):
    """Calculation of arguments for jedicolor.


The weights for bulge narrowbands are calculated using following eqn:

.. math:: b[0] = \\frac{\\int_{\\lambda0}^{\\lambda1} f_b(\\lambda)d\\lambda}{\\int_{\\lambda0}^{\\lambda_{20}} f_b(\\lambda)d\\lambda}

.. math:: b[0] = \\frac{Ilb}{Ilbt}

.. math:: Ilb = \int_{\lambda0}^{\lambda1} f_b(\lambda)d\lambda

.. math:: Ilbt = \int_{\lambda0}^{\lambda_{20}} f_b(\lambda)d\lambda

Similarly, the weights for disk narrrowbands are calcluated like this:

.. math:: d[0] = \\frac{\\int_{\\lambda0}^{\\lambda1} f_d(\\lambda)d\\lambda}{\\int_{\\lambda0}^{\\lambda_{20}} f_d(\\lambda)d\\lambda}

.. math:: d[0] = \\frac{Ild}{Ildt}

.. math:: Ild = \int_{\lambda0}^{\lambda1} f_d(\lambda)d\lambda

.. math:: Ildt = \int_{\lambda0}^{\lambda_{20}} f_d(\lambda)d\lambda

    """

    # Wavelenths
    laml, lamh = wavelengths(config)
    # print('laml = \n', laml )
    # print('lamh = \n', lamh )

    # LSST r band 6 Gyr old integrals for bulge and disk (LSST has narrowbands)
    Ilb  = [integrate_flux(infileb, laml[i], laml[i+1]) for i in range(21) ]
    Ild  = [integrate_flux(infiled, laml[i], laml[i+1]) for i in range(21) ]
    # for i in range(len(Ilb)): print(Ilb[i],Ild[i])

    # LSST r band 6 Gyr old total range integrals for bulge and disk
    Ilbt =   integrate_flux(infileb, laml[0], laml[21])
    Ildt =   integrate_flux(infiled, laml[0], laml[21])

    # bulge and disk weights
    b  = np.array(Ilb) / Ilbt
    d  = np.array(Ild) / Ildt

    # Write bd_weights.csv
    print('\nWriting: %s\n'%(outfile))
    np.savetxt(outfile, np.array([b,d]).T, fmt=[str('%.5f'), str('%.5f')], delimiter='\t')

    # debug
    # print("len(Ilb) = {}".format(len(Ilb)))
    # print("Ilbt = {}".format(Ilbt))


def main():
    # Usage: python a3_bd_weights.py -z 1.5
    # Runtime: 1.6 sec

    # Config parameters
    config = updated_config('physics_settings/configb.sh')
    z = float(config['fixed_redshift'])

    # Variables
    infileb = 'sed/ssp_pf_interpolated_z{}.csv'.format(z)
    infiled = 'sed/exp9_pf_interpolated_z{}.csv'.format(z)
    outfile  = 'physics_settings/bd_weights_z{}.txt'.format(z)

    # Run the main program
    write_bd_weights(config, infileb,infiled,outfile)


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
