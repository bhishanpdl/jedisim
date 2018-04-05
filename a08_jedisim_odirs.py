#!python
# -*- coding: utf-8 -*-#
###########################################################################
# Author      : Bhishan Poudel; Physics Graduate Student, Ohio University
# Date        : Sep 18, 2017
# Last update :
###########################################################################
"""
:Topic: Create output directories for jedisim.

This program deletes old outputs folders and created new empty ones.
It creates folders for both unrotated and rotated cases.

Following folders will be created:

  - jedisim_out/out0/scaled_bulge scaled_disk scaled_bulge_disk
  - jedisim_out/out0/convolved/
  - jedisim_out/out0/scaled_bulge/ distorted_0_to_12/ for scaled_bulge scaled_disk scaled_bulge_disk
  - jedisim_out/out0/scaled_bulge/transformed_0_to_12/ for scaled_bulge scaled_disk scaled_bulge_disk

:Runtime: 8 sec (Oct 2, 2017 Pisces)

"""

# Imports
from __future__ import print_function, unicode_literals, division, absolute_import, with_statement
import os
import sys
import subprocess
import math
import re
import shutil
import copy
import time
import numpy as np
from util import replace_outfolder, run_process, updated_config

def replace_outfolders_jedi(config_path):
    """Replace old output folders before running new simulation.
    
    The names transformed and distorted are used inside jeditransform.c.
    And, they are not read from config file.
    """
    config = updated_config(config_path)
    outfolders = [config["output_folder"][0:-1],
                  config['output_folder']+ 'convolved/'
                  ]
    for outfolder in outfolders:
        replace_outfolder(outfolder)

    # Make stamps and distorted folders
    # e.g. jedisim_out/out0/transformed_0 to transformed_12
    # e.g. jedisim_out/out0/distorted_0 to distroted_12
    for x in range(0, int(math.ceil(float(config['num_galaxies']) / 1000))):
        postage_path   = config['output_folder'] + "transformed_"     + str(x)
        distorted_path = config['output_folder'] + "distorted_" + str(x)
        if not os.path.exists(postage_path):
            os.makedirs(postage_path)
        if not os.path.exists(distorted_path):
            os.makedirs(distorted_path)

def d90_replace_outfolders_jedi(config_path):
    """Replace old output folders before running new simulation."""
    config = updated_config(config_path)
    outfolders = [config["90_output_folder"],
                  config['90_output_folder']+ 'convolved/'
                  ]
    for outfolder in outfolders:
        replace_outfolder(outfolder)

    # Make stamps and distorted folders
    # e.g. jedisim_out/out90/transformed_0 to transformed_12
    # e.g. jedisim_out/out90/distorted_0 to distorted_12
    for x in range(0, int(math.ceil(float(config['num_galaxies']) / 1000))):
        postage_path   = config['90_output_folder'] + "transformed_"     + str(x)
        distorted_path = config['90_output_folder'] + "distorted_" + str(x)
        if not os.path.exists(postage_path):
            os.makedirs(postage_path)
        if not os.path.exists(distorted_path):
            os.makedirs(distorted_path)


def main():
    """Run main function."""
    # Runtime: 10 sec

    # Create output folders.
    config_paths = ['physics_settings/config{}.sh'.format(i) for i in list('bdm') ]
    for config_path in config_paths:
        replace_outfolders_jedi(config_path)
        d90_replace_outfolders_jedi(config_path)


if __name__ == "__main__":
    #  Run the main program
    main()
