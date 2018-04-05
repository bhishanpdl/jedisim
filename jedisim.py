#!python
#-*- coding: utf-8 -*-
"""
:Author: Bhishan Poudel, Physics PhD Student, Ohio University

:Date:

  |today|

"""
# Imports
from __future__ import print_function, with_statement, division, unicode_literals, absolute_import
from astropy.cosmology import FlatLambdaCDM
import os
import sys
import subprocess
import math
import re
import shutil
import copy
import time
import numpy as np
from util import run_process

def jedimaster():
    # Run jedisim programs
    # NOTE: before running this program config files and psf should be created
    #       using other programs a01 to a07 once.
    #       The programs a01-a07 runs only once, however,
    #       this jedimaster runs in a loop for multiple times, maybe 100 times.
    #
    run_process("Create outdirs     for 0 & 90 deg", ['python', "a08_jedisim_odirs.py"])
    run_process("Create  3 catalogs for 0 & 90 deg", ['python', "a09_jedisim_3cats.py"])
    run_process("Run the simulation for 0 degree.",  ['python', "a10_jedisimulate.py"])
    run_process("Run the simulation for 90 degree.", ['python', "a11_jedisimulate90.py"])

def main():
    """Run main function."""
    jedimaster()

if __name__ == "__main__":
    main()
