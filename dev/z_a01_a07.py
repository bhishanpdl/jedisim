#!python
# -*- coding: utf-8 -*-
"""
Run python scripts from a01 to a07.

:Author:  Bhishan Poudel; Physics Graduate Student, Ohio University

:Date: Aug 01, 2016

:Last update: Oct 2, 2017

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
from util import run_process,updated_config,replace_outfolder

# start time
start_time = time.time()
start_ctime = time.ctime()

def main():
    """Run main function."""
    os.system('python a01_jedisim_config.py -z 1.5') # 0.6 sec
    os.system('python a02_interpolate_sed.py') # 3 secs
    os.system('python a03_scaled_bd_factors.py') # 38 seconds.
    os.system('python a04_scaled_gals.py') # 1 minutes, 30 seconds.
    os.system('python a05_bd_weights_psf.py') # 3.5 seconds.
    os.system('python a06_scaled_bd_flux_rat.py') # 28 secs.
    os.system('python a07_psf_bdmono.py') # 10 secs.


if __name__ == "__main__":
        import time, os

        # Beginning time
        program_begin_time = time.time()
        begin_ctime        = time.ctime()

        #  Run the main program
        main()

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
        print("End of Program: {}".format(os.path.basename(__file__)))
        print("\n")
