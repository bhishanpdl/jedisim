#!python
# -*- coding: utf-8 -*-#
"""
Check negative pixels in a fitsfile.
    
@author: Bhishan Poudel
    
@date:  Mar 28, 2018
    
"""
# Imports
import numpy as np
from astropy.io import fits


def find_all_negs_gals(mypath):
    negs=[]
    for i in range(201):
        try:
            dat = fits.getdata('{}{}.fits'.format(mypath, i))
            print(i)
        except:
            dat = np.array([])
            
        mysum = np.sum(dat)
        fname = '{}{}.fits'.format(mypath, i)
            
        # check for neg pixel            
        neg_idx = np.argwhere(dat < 0)
        
        if len(neg_idx) != 0:
            # print("neg_idx = {}".format(neg_idx))
            print('ERROR: Negative Pixels found in: ', fname)
            negs.append(i)
        
            
    return negs

def check_path():
    bulge = 'bulge_f8/f814w_bulge'
    disk = 'disk_f8/f814w_disk'
    
    
    mypath = bulge
    # mypath = disk
    
    negs = find_all_negs_gals(mypath)
    print(negs)
    print(len(negs))



if __name__ == "__main__":
    check_path()
