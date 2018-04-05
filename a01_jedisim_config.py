#!python
# -*- coding: utf-8 -*-
#
###########################################################################
# Author      : Bhishan Poudel; Physics Graduate Student, Ohio University
# Date        : Jun 10, 2017 Sat
# Last update :
###########################################################################
"""
Create config.sh files according to the redshift using the given template.

:Command: python a01_jedisim_config.py -z 1.5

:Depends: physics_settings/config_template.sh

:Outputs: physics_settings/
    
    -configb.sh 
    -configd.sh 
    -configm.sh 
    -lens.txt

:Runtime: 0.6 sec.

"""
# Imports
from __future__ import print_function, unicode_literals, division, absolute_import, with_statement
import os
import time
import sys
import argparse
from util import config_dict

# Global variable
NUM_GALS = 201

def gen_config(z,config_template,scaled_bd,config_path):
    """ Generate the config file for jedisim from given template.

    Args:
      z (str): Redshift of the base galaxy. e.g. 1.5
      config_template (str): Template file to use will almost all the physics used
      scaled_bd (str): string 'scaled_bulge' or 'disk'.
      config_path (str): output config file. e.g. configb.sh or configd.sh

    .. note::

       This needs template_config.sh input text file.

    """
    # data
    data = open(config_template).readlines()
    print('For redshift %.1f Creating : %s'%(z, config_path))
    with open(config_path, 'w') as fo:
        for line in data:
            # conditions
            c1 = line.lstrip().startswith('bd_weights')
            c2 = line.lstrip().startswith('bd_flux_rat')
            c3 = line.lstrip().startswith('fixed_redshift')
            c4 = line.lstrip().startswith('output_folder')
            c5 = line.lstrip().startswith('90_output_folder')

            if not (c1 or c2 or c3 or c4 or c5):
                fo.write(line)

            if c1:
                # from: bd_weights="physics_settings/bd_weights.txt"
                # to: bd_weights="physics_settings/bd_weights_z1.5.txt"
                line = line.replace("bd_weights.txt","bd_weights_z{}.txt".format(z))
                fo.write(line)

            if c2:
                # from: bd_weights="physics_settings/bd_weights.txt"
                # to: bd_weights="physics_settings/bd_weights_z1.5.txt"
                line = line.replace("settings/bd_flux_rat","settings/bd_flux_rat_z{}".format(z))
                fo.write(line)

            if c3:
                # from: fixed_redshift=1.5  # the single source galaxy redshift to use
                # to: fixed_redshift=1.0  # the single source galaxy redshift to use
                line = line.replace("fixed_redshift=1.5","fixed_redshift={}".format(z))
                fo.write(line)

            if c4:
                # from: output_folder="jedisim_out/out0/"
                # to: output_folder="jedisim_out/out0/scaled_bulge/"
                line = line.replace("jedisim_out/out0/","jedisim_out/out0/{}/".format(scaled_bd))
                fo.write(line)

            if c5:
                # from: 90_output_folder="jedisim_out/out90/"
                # to: 90_output_folder="jedisim_out/out90/scaled_bd/"
                line = line.replace("jedisim_out/out90/","jedisim_out/out90/{}/".format(scaled_bd))
                fo.write(line)


    ## add image names at the bottom of the config file (jedicatalog will read these.)
    with open(config_path, 'a') as fo:
        for i in range(NUM_GALS):
            line = r'image="simdatabase/{0:}_f8/f814w_{0:}{1:d}.fits"'.format(scaled_bd,i) + '\n'
            fo.write(line)


def gen_config_files(z,config_template):
    """Create config files for bulge, disk and bulge_disk."""

    # For scaled bulge
    scaled_bd = 'scaled_bulge'
    config_path = 'physics_settings/configb.sh'
    gen_config(z,config_template,scaled_bd,config_path)

    # For scaled disk
    scaled_bd = 'scaled_disk'
    config_path = 'physics_settings/configd.sh'
    gen_config(z,config_template,scaled_bd,config_path)

    # For scaled bulge_disk
    scaled_bd = 'scaled_bulge_disk'
    config_path = 'physics_settings/configm.sh'
    gen_config(z,config_template,scaled_bd,config_path)

def gen_lens_file(lens_file,x,y,lens_type,p1,p2):
    """Create config files for bulge, disk and bulge_disk."""
    print("Creating: {}".format(lens_file))

    with open(lens_file,'w') as fo:
        fo.write('{:d} {:d} {:d} {:.2f} {:.2f}'.format(int(x),int(y),int(lens_type),float(p1),float(p2)))



def main():
    """Run main function."""
    # Usage: python a01_jedisim_config.py -z 1.5
    parser = argparse.ArgumentParser('Create bulge disk weights text file.')
    parser.add_argument('-z', '--redshift',
                        type=float,
                        default='1.5',
                        help='Redshift of the simulated galaxy.')
    FLAGS, unparsed = parser.parse_known_args()

    # Variables
    config_template = 'physics_settings/template_config.sh'
    z = FLAGS.redshift

    # Generate config files
    gen_config_files(z,config_template) # physics_settings/configb.sh, configd.sh and configm.sh

    # Now generate lens file for jedidistort.
    config = config_dict(config_template)
    lens_file = 'physics_settings/lens.txt'
    x = config['lens_x']
    y = config['lens_y']
    lens_type = config['lens_type']
    p1 = config['lens_p1']
    p2 = config['lens_p2']
    gen_lens_file(lens_file,x,y,lens_type,p1,p2) # physics_settings/lens.txt


##==============================================================================
## Main program
##==============================================================================

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
