#!python
# -*- coding: utf-8 -*-
#
# Author      : Bhishan Poudel; Physics PhD Student, Ohio University
# Date        : Jun 09, 2017 Fri
"""
Get interpolated sed files for bulge and disk with 1 Angstrom wavelength stepsize.

:Depends: Following are the dependences
  - sed/ssp_pf.cat
  - sed/exp9_pf.cat

:Outputs: Following are the outputs
  - sed/ssp_pf_interpolated_z1.5.cat
  - sed/exp9_pf_interpolated_z1.5.cat

:Sed file: The sed file have wavelength and flux values for exp disk we have::

    # Wavelen 1Gyr         2Gyr         3Gyr         4Gyr         5Gyr
    # lambda  flux[0]      flux[1]      flux[2]      flux[3]      flux[4]
    1000    2.125075e-05 1.905875e-05 1.706275e-05 1.527475e-05 1.36735e-05

    # Wavelen 6Gyr       7Gyr         8Gyr       9Gyr        10Gyr     11Gyr       12Gyr
    # lambda  flux[5]    flux[6]      flux[7]    flux[8]     flux[9]   flux[10]    flux[11]
    1000    1.224e-05  1.095675e-05 9.8095e-06 8.78425e-06 7.868e-06 7.04975e-06 6.319e-06



    Age of Universe for z =  0.0 is  13.47 Gyr
    Age of Universe for z =  1.5 is  4.20 Gyr
    Age of Universe for z =  4.0 is  1.52 Gyr
    Difference                   is  2.68 Gyr
    Age of Galaxy   for z =  1.5 is     3 Gyr

    If the galaxy was born at z=4, the z=1.5 will have age 3 Gyr.

:Command: python a02_interpolate_sed.py

:Runtime:  3 sec.

"""
# Imports
from __future__ import print_function, unicode_literals, division, absolute_import, with_statement
from astropy.cosmology import FlatLambdaCDM
import util
import numpy as np
import scipy as sp
import scipy.interpolate
import time, os,sys
from util import updated_config


def interpolate_flux(config, infile, outfile,lambda1,lambda2):
    """ Interpolate the sed file in step of 1 Angstrom."""
    z    = float(config['fixed_redshift'])
    age1 = util.age(z) - util.age(4.0)
    age  = abs(int(round(age1))) # Nearest Gyr

    # Get columns of sed file.
    wave, flux_z, flux12 = np.loadtxt(infile, skiprows=15, unpack=True,
                                   dtype='float', usecols=(0, age, 12))

    # wavelength range to interpolate
    nums = int(lambda2 - lambda1) + 1
    waverange = np.linspace(lambda1, lambda2, num=nums, endpoint=True)


    # interpolation
    #print('{} {} {}'.format('\nInterpolating flux from the file : ', infile, ' \n...'))
    iflux_z = sp.interpolate.interp1d(wave, flux_z, kind='cubic')(waverange)
    iflux12 = sp.interpolate.interp1d(wave, flux12, kind='cubic')(waverange)


    # write to a file
    # second column must be flux_z, it will be read by another program.
    hdr = '%-14s %-14s %+18s'%('wavelength', 'flux_z'.format(age), 'flux12')
    np.savetxt(outfile, list(map(list, zip(*[waverange, iflux_z, iflux12]))),
               fmt=['%-13d','%.13e','%.13e'], delimiter='\t', newline='\n',
               header=hdr)


    # output info
    print('Interpolating from %d to %d from file: %s' % (lambda1,lambda2,infile) )
    print('Writing interpolated file to:', outfile, '\n')

    # Galaxy and Universe Ages
    print( 'Age of Universe for z = {:4.1f} is  {:4.2f} Gyr'.format(0, util.age(0)))
    print( 'Age of Universe for z = {:4.1f} is  {:4.2f} Gyr'.format(z, util.age(z)))
    print( 'Age of Universe for z = {:4.1f} is  {:4.2f} Gyr'.format(4, util.age(4)))
    print( 'Difference                   is  {:4.2f} Gyr'.format( util.age(z) - util.age(4)))
    print( 'Age of Galaxy   for z = {:4.1f} is  {:4d} Gyr'.format(z,age))

    #print('{} {} {}'.format('\ninterpolation range :',  waverange, '\n'))
    #print('{} {} {}'.format('input file            : ', infile, ''))
    #print('{} {} {}'.format('output file           :',  outfile, ''))

def main():

    # Global Variables
    config_path = 'physics_settings/configb.sh'
    config      = updated_config(config_path)
    lambda1     = 1000
    lambda2     = 12000
    infileb     = 'sed/ssp_pf.cat'
    infiled     = 'sed/exp9_pf.cat'

    # Derived names
    z        = float(config['fixed_redshift'])
    outfileb = 'sed/ssp_pf_interpolated_z{}.csv'.format(z)
    outfiled = 'sed/exp9_pf_interpolated_z{}.csv'.format(z)

    # Parameters
    age = util.age(4.0) - util.age(z)
    age = int(round(age)) # Nearest Gyr
    age = age - 1 # column 0 is 1 Gyr
    age = abs(age)

    # Interpolate
    interpolate_flux(config, infileb, outfileb,lambda1,lambda2)
    interpolate_flux(config, infiled, outfiled,lambda1,lambda2)

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
