#!python
# -*- coding: utf-8 -*-#
"""
Split a large file into small parts.
    
Author : Bhishan Poudel
Date   :  Apr 5, 2018
    
"""
# Imports
import os
import glob

def split_psf():
    for f in glob.glob('*.fits'):
        cmd = 'split -b40m {} {}'.format(f,f.strip('.fits'))
        print("\n")
        print('Splitting: {}'.format(f))
        print("cmd = {}".format(cmd))
        os.system(cmd)


def combine_psf():
    if not os.path.isdir('orig_psf'):
        os.makedirs('orig_psf')
        
    for i in range(21):
        cmd = 'cat psf{}a? > orig_psf/psf{}.fits'.format(i,i)
        print("cmd = {}".format(cmd))
        os.system(cmd)
        
    for i in list('bdm'):
        cmd = 'cat psf{}a? > orig_psf/psf{}.fits'.format(i,i)
        print("cmd = {}".format(cmd))
        os.system(cmd)
        

        
def main():
    """Run main function."""
    # split_psf()
    combine_psf()
    
if __name__ == "__main__":
    main()
