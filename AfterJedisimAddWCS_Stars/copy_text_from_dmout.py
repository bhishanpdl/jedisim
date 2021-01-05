from __future__ import print_function, division
import os
import sys
import shutil

z = sys.argv[1]
dmout = sys.argv[2]
odir = 'txt10_' + dmout

if not os.path.isdir(odir):
    os.makedirs(odir)

for l in ['lsst', 'lsst90', 'lsst_mono', 'lsst_mono90']:
    for i in range(10):
        ifile = dmout + '/' + l + '/' + 'dmstack_output/' +\
                'dm_out_z{}_{}/'.format(z,l) +\
                'txt_{}_z{}/'.format(l,z) +\
                'src_{}_z{}_{:03d}.csv'.format(l,z,i)

        ofile = odir + '/' + l + '_{:03d}.csv'.format(i)
        print(ifile)
        print(ofile)
        try:
            shutil.copyfile(ifile,ofile)
        except:
            pass


# PURPOSE: copy some dmstack output text files of last and mono into a new folder
#
# command: python copy_text_from_dmout.py 1.5 wcs_star_jout_z1.5_000_099
# output : txt10_wcs_star_jout_z1.5_000_099  with 10 * 4 text files
#
# after this: we copy text files to Pisces and do after dmstack analysis
# we will remove nans and use IMCAT on that text file.