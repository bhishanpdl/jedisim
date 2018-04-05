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
import numpy as np
import sys
from astropy.io import fits


def find_negs_in_path(mypath):
    # get nan values
    mynans = []
    negs=[]
    zeros = []
    for i in range(201):
        dat = fits.getdata('{}{}.fits'.format(mypath, i))
        mysum = np.sum(dat)
        fname = '{}{}.fits'.format(mypath, i)
        # print(fname , 'has sum = ', mysum)
                
        # check for nan
        if np.isnan(mysum):
            mynans.append(i)
            print("mynans = {}".format(mynans))
            sys.exit(1)
                
        # check for neg pixel            
        neg_idx = np.argwhere(dat < 0)
        
        if len(neg_idx) != 0:
            print("neg_idx = {}".format(neg_idx))
            print('ERROR: Negative Pixels found in: ', fname)
            sys.exit(1)
        
        # check for zero sum
        if float(mysum) == 0.0:
            zeros.append(i) 
        
    # prints
    print("zeros = {}".format(zeros))
    print("len(zeros) = {}".format(len(zeros)))      
            
    return mynans,neg_idx, zeros
    
#
def find_negs_in_fits(myfits):
    dat = fits.getdata(myfits)
    
    # check nan
    mysum = np.sum(dat)
    
    # check negative pixels
    neg_idx = np.argwhere(dat < 0)
    print("\n")
    print('Negative indices = ', neg_idx)
    print('File : ', myfits)
    print('Sum  : ', mysum)
    
    if np.isnan(mysum):
        print("ERROR: NaN found in: ", myfits)
        sys.exit(1)
    
    if mysum == 0.0:
        print("ERROR: Total sum is ZERO in : ", myfits)
        sys.exit(1)
    
    if len(neg_idx) !=0:
        x,y = neg_idx[-1]
        print('Index: ', x,y, '# For ds9 X,Y = ', y+1,x+1)
        print('Value: ', dat[x,y])
        sys.exit(1)
    
    
def check_path():
    bulge = 'simdatabase/bulge_f8/f814w_bulge'
    disk = 'simdatabase/disk_f8/f814w_disk'
    scaled_bulge = 'simdatabase/scaled_bulge_f8/f814w_scaled_bulge'
    scaled_disk = 'simdatabase/scaled_disk_f8/f814w_scaled_disk'
    mypaths = [bulge,disk,scaled_bulge,scaled_disk]
    mypaths = [scaled_bulge]
    mypaths = [scaled_disk]
    for mypath in mypaths:
        mynans,neg_idx, zeros = find_negs_in_path(mypath)


def check_files():
    # scaled bulge
    sb_hst = 'jedisim_out/out0/scaled_bulge/trial1_HST.fits'
    sb_lsst = 'jedisim_out/out0/scaled_bulge/trial1_lsst_bulge.fits'
    
    # scaled disk
    sd_hst = 'jedisim_out/out0/scaled_disk/trial1_HST.fits'
    sd_lsst = 'jedisim_out/out0/scaled_disk/trial1_lsst_disk.fits'
    
    # scaled bulge-disk
    sbd_hst = 'jedisim_out/out0/scaled_bulge_disk/trial1_HST.fits'
    sbd_lsst_bd = 'jedisim_out/out0/scaled_bulge_disk/trial1_lsst_bulge_disk.fits'
    sbd_lsst = 'jedisim_out/out0/scaled_bulge_disk/trial1_lsst.fits'
    sbd_mono = 'jedisim_out/out0/scaled_bulge_disk/trial1_lsst_mono.fits'
    
    
    myfits = [sb_hst, sb_lsst, sd_hst, sd_lsst, sbd_hst, sbd_lsst_bd, sbd_lsst, sbd_mono]
    myfits = [sb_hst]
    myfits = [sbd_lsst_bd]
    
    for myfit in myfits:
        find_negs_in_fits(myfit)


def check_distorted():
    # scaled bulge
    dis = 'jedisim_out/out0/scaled_bulge'
    
    for i in range(12):
        for j in range(i*1000,i*1000+1000):
            myfit = '{}/distorted_{}/distorted_{}.fits'.format(dis,i,j)
            find_negs_in_fits(myfit)

def check_transformed():
    # scaled bulge
    head = 'jedisim_out/out0/scaled_bulge'
    fname = head + '/' + 'transformed_0/transformed_3.fits.gz'
    dat = fits.getdata(fname)
    mysum = np.sum(dat)
    print("mysum = {}".format(mysum))
    
    pos_idx = np.argwhere(dat > 0)
    print("pos_idx = {}".format(pos_idx))


if __name__ == "__main__":
    # check_path()
    check_files()
    # check_distorted()
    # check_transformed()
