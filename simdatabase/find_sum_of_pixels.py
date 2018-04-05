#!python
# -*- coding: utf-8 -*-#
#
# Author      : Bhishan Poudel; Physics Graduate Student, Ohio University
# Date        : Jan 4, 2017
# Update      : Aug 7, 2017 Mon
# 
# Imports
import os
import subprocess
import glob
import re
import natsort
from astropy.io.fits import getdata
import numpy as np

def find_nan_in_fits(headname):
    """Check if a fitsfile has nan values in it.
    
    Parameters:
    ------------
     headname: full path name without .fits 
             e.g. disk_f8
             
    """
    # get nan values
    mysums = []
    mynans = []
    negs=[]
    zeros = []
    non_zeros = []
    for i in range(201):
        dat = getdata('{}{}.fits'.format(headname, i))
        mysum = np.sum(dat)
        mysums.append(mysum)
        if np.isnan(mysum):
            mynans.append(i)
            # print('simdatabase/bulge_disk_f8/bdf8_{}.fits'.format(i) , 'has sum = ', mysum)
        # print('{}{}.fits'.format(headname, i) , 'has sum = ', mysum)
        
        # extra
        if float(mysum) < 0.0:
            negs.append(i)
        if float(mysum) == 0.0:
            zeros.append(i)
                  
    return mynans,negs, zeros, mysums

if __name__ == "__main__":
    
    # headname is name withot number.fits
    # headname = 'bulge_f8/f814w_bulge'
    headname = 'disk_f8/f814w_disk'
    mynans,negs, zeros, mysums = find_nan_in_fits(headname)
    
    print("mynans = {}".format(mynans))
    print("negs = {}".format(negs))
    # print("zeros = {}".format(zeros))
    print("len(zeros) = {}".format(len(zeros)))
    
    non_zeros = [i for i in mysums if i !=0.0]
    # print("non_zeros = {}".format(non_zeros))
    print("min(non_zeros) = {}".format(min(non_zeros)))
    
    for i, n in enumerate(mysums):
        if n!=0 and n<2.0:
            print("galaxy = {} and sum = {}".format(i, n))


"""Outputs
For scaled bulge:
mynans = []
negs = []
zeros = []

For scaled_disk:
mynans = []
negs = []
zeros = [7, 10, 11, 12, 18, 25, 27, 35, 37, 38, 39, 40, 43, 46, 47, 48, 54, 61, 
65, 66, 68, 73, 79, 80, 81, 85, 88, 93, 94, 95, 99, 100, 102, 103, 106, 107, 
108, 110, 112, 113, 114, 115, 116, 117, 120, 121, 123, 126, 129, 137, 142, 
145, 146, 148, 149, 152, 161, 163, 164, 165, 166, 167, 168, 170, 175, 177, 
183, 184, 186, 192, 195, 196]
len(zeros) = 72

galaxy = 56 and sum = 1.2959390878677368
galaxy = 87 and sum = 1.4832329750061035
galaxy = 97 and sum = 1.8003742694854736
galaxy = 104 and sum = 1.9017444849014282
galaxy = 105 and sum = 0.8677717447280884
galaxy = 127 and sum = 0.8214941620826721
galaxy = 136 and sum = 1.061703085899353
galaxy = 139 and sum = 1.633044719696045
galaxy = 159 and sum = 1.8048251867294312
galaxy = 190 and sum = 1.168720006942749

"""
