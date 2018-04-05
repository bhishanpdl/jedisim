# This is the config file for jedisim.py and associated programs.
#
# Conventions used in this file: 
# 1) There should be no empty lines in this file.
# 2) values should be enclosed by ""  not ''.
# 3) There should not be spaces around = sign.
#
# key=float_value  or key="string_value"    
# DO NOT USE THESE:   key = value  or  key='value'
#
#------------------------------ bulge disk factor ------------------------------
# Ref: https://www.lsst.org/about/camera/features
# Ref: http://www.stsci.edu/hst/acs/documents/handbooks/current/c05_imaging2.html
LSST_r_blue_wavelength=5520 # Angstrom (bd_factors_scaled.py and bd_weights_psf.py)
LSST_r_red_wavelength=6910 # Angstrom (bd_factors_scaled.py and bd_weights_psf.py)
HST_ACS_WFC_central_wavelength=8333 # Angstrom for Broad I WFC camera.
HST_ACS_WFC_width=2511 # Angstrom
z_cutout=0.2
#
#
#------------------------------ jedicatalog --------------------------------------
# jedicatalog will read MAG,MAG0,PIXSCALE, and RADIUS from the input fitsfiles and
# will create three catalogs:  catalog.txt,convolved.txt,distortedlist.txt
# To create these files jedicatalog needs some physics settngs quantities
# which are given below.
# These setting will also be other programs.
#----------------------------- physics settings --------------------------------
nx=12288            # x pixels            (arg for jedidistort)
ny=12288            # y pixels            (arg for jedidistort)
pix_scale=0.06      # arseconds per pixel (arg for jedidistort)
lens_z=0.3          # lens redshift       (arg for jedidistort)
single_redshift=1   # 0 = not-fixed, 1=fixed
fixed_redshift=0.7  # the single source galaxy redshift to use (bdfactors, bdweights)
final_pix_scale=0.2 # LSST pixscale (arcsecords per pixel)
exp_time=6000       # exposure time in seconds
noise_mean=10       # mean for poisson noise
x_border=301        # must be large enough so that no image can overflow_
y_border=301        # must be large enough so that no image can overflow
x_trim=480          # larger than x_border to ensure no edge effects
y_trim=480          # larger than y_border to ensure no edge effects
num_galaxies=20000  # number of galaxies to simulate 138,000 default
min_mag=22          # minimum magnitude galaxy to simulate (inclusive)
max_mag=28          # maximum magnitude galaxy to simulate (inclusive)
power=0.33          # power for the power law galaxy distribution
# For the f814 filter for our 201 galaxy images
#minmag   =  19.4715 # f814w_gal_19.fits
#maxmag   =  25.9455 # f814w_gal_214.fits
# For the HST galaxies cut outs we have magnitude range from 19-26.
# Note that we do not have the file radius database 19.txt
# inside simdatabase/radius_db/ so jedicatalog will fail if we take min_mag 19.
# However, we are not interested in simulation of mag 19.
# We are interested in fainter LSST galaxies with range 22-28 right now.
#---------------------------- Lens for jedidistort  ----------------------------
# lens.txt has a single line with 5 parameters
# 6144 6144 1 1000.000000 4.000000
#  x    y  type p1       p2
#  x - x center of lens (in pixels)
#  y - y center of lens (in pixels)
#  type - type of mass profile
#         1. Singular isothermal sphere
#         2. Navarro-Frenk-White profile
#	        3. NFW constant distortion profile for grid simulations
#  p1 - first profile parameter
#         1. sigma_v [km/s]
#         2. M200 parameter [10^14 solar masses]
#		      3. Distance to center in px. M200 fixed at 20 default,
#            which can be modified in case 3
#  p2 - second profile parameter
#         1. not applicable, can take any numerical
#         2. c parameter [unitless]
#         3. c parameter [unitless]
lens_x=6144
lens_y=6144
lens_type=1
lens_p1=1000.0
lens_p2=4.0
lens_file="physics_settings/lens.txt"	  # arg for jedidistort
#----------------------- Output Folders ----------------------------------------
# Note that for scaled_bulge, output folder is jedisim_out/out0/scaled_bulge
output_folder="jedisim_out/out0/scaled_disk/"         # jedicatalog etc.
90_output_folder="jedisim_out/out90/scaled_disk/"  # jedicatalog etc.
prefix="trial1_" # used by jedicatalog etc.
#----------------------- HST images from jediconvolve --------------------------
# Note that HST and LSST will be updated to trial1_HST.fits and
# trial1_LSST_averaged.fits and so on.
HST_image="HST.fits"                      # jedipaste, jediconvolve
HST_convolved_image="HST_convolved.fits"  # jedipaste2, jedirescale
#----------------------- database folders --------------------------------------
# There are 10 radius database files 20.dat to 29.dat.
# which contains min and max radius to be used by jedicatalog.
# e.g. the file simdatabase/radius_db/20.dat has two lines: 36.72 3.51
# This must contain files "n.txt" for n= min_mag to max_mag
radius_db_folder="simdatabase/radius_db/"
# There are 15+2 redshift database files 19.dat to 33.dat with +- 99.dat.
# which contains min and max redshift to be used by jedicatalog.
# e.g. the file simdatabase/red_db/19.dat has two lines: 0.301000 0.138000
# For f814 filter images:
# minmag   =  19.4715 # f814w_gal_19.fits
# maxmag   =  25.9455 # f814w_gal_214.fits
# minrad   =  1.31    # f814w_gal_43.fits
# maxrad   =  21.895  # f814w_gal_9.fits
# For f606 filter images:
# minmag =  19.3882 # f606w_gal120.fits
# maxmag =  25.5268 # f606w_gal215.fits
# minrad =  1.157   # f606w_gal93.fits
# maxrad =  22.055  # f606w_gal110.fits
red_db_folder="simdatabase/red_db/"
#------------------- bulge to disk weights -------------------------------------
# This file will be updated by jedisim_ofiles.py to:
# bd_weights="physics_settings/bd_weights_z1.5.txt" or so on.
bd_weights="physics_settings/bd_weights_z0.7.txt" # jedisim_config, jedisimulate
bd_factors="physics_settings/bd_factors.txt" # jedisim_config, jedisimulate
bd_flux_rat="physics_settings/bd_flux_rat_z0.7.txt" # fr, frb, frd written by scaled_bd_flux_rat.py
#------------------- rescaled outfiles for jedirescale -------------------------
rescaled_outfileb="lsst_bulge.fits" # jedisimulate.py  (gcsb galaxy convolved rescaled)
rescaled_outfiled="lsst_disk.fits" # jedisimulate.py
rescaled_outfilem="lsst_bulge_disk.fits" # jedisimulate.py
#--------------------- Final outputs of jedisim -------------------------------
lsst_unnoised="lsst_unnoised.fits" # jedisimulate.py
lsst="lsst.fits" # jedisimulate.py
lsst_mono="lsst_mono.fits" # jedisimulate.py
#------------------- psf files for jediconvolve --------------------------------
psfb="psf/psfb.fits"
psfd="psf/psfd.fits"
psfm="psf/psfm.fits"
#------------------- catalog files for jedicatalog -----------------------------
# jedicatalog will read four headers MAG, MAG0, PIXSCALE, RADIUS from
# the images given in the end of this config.sh file.
#
# jedicatalog will write the following quantity needed by jeditransform in
# the file jedisim_out/out0/trial1_catalog.txt:
# name,x,y,angle,redshift,pixscale,old_mag,old_rad,new_mag,new_rad,stamp_name,dis_name
#
# jedicatalog also creates the catalog list for the program jediconvolve:
# jedisim_out/out0/trial1_convolvedlist.txt
#
# This text files have 6 rows:
# jedisim_out/out1/convolved/convolved_band_0.fits
# jedisim_out/out1/convolved/convolved_band_5.fits
#
# jedicatalog also creates the catalog list for the program jedidistort:
# jedisim_out/out0/trial1_distortedlist.txt
#
# This text file 12420 rows.
# There are 13 folder names and each folder name has 1000 filenames except last.
# The contents of distortedlist.txt is like this:
# line     1: jedisim_out/out0/distorted_0/distorted_0.fits
# line 12420: jedisim_out/out0/distorted_12/distorted_12419.fits
#
# The code snippets used in jedicatalog is:
# else if(strcmp(buffer3,"catalog_file")==0) sscanf(buffer2, "catalog_file=\"%[^\"]", temp_catalog_file);
#
# Three text files created by jedicatalog are:
# jedisim_out/out0/scaled_bulge/trail1_catalog.txt
# jedisim_out/out0/scaled_bulge/trail1_convolvedlist.txt
# jedisim_out/out0/scaled_bulge/trail1_distortedlist.txt
catalog_file="catalog.txt"
convolvedlist_file="convolvedlist.txt"
distortedlist_file="distortedlist.txt"
#----------------- catalog files for jedidistort -------------------------------
# jeditransform creates jedisim_out/out0/scaled_bulge/trial1_dislist.txt along with 12420 .gz stamps
# jedidistort will use these files.
# Input galaxy parameter file for jedidistort: x y nx ny zs file
#           x - x coord. of lower left pixel where galaxy should be embedded
#           y - y coord. of lower left pixel where galaxy should be embedded
#           nx - width of the galaxy in pixels
#           ny - height of the galaxy in pixels
#           zs - redshift of this galaxy
#           infile - filepath to the FITS file for this galaxy, 1024 chars max
#           outfile - filepath for the output FITS file for this galaxy, 1024 chars max
#
#  e.g. jedisim_out/out1/dislist.txt looks like this: (was created by jeditransform)
# 6813 888 10 23 1.500000 jedisim_out/out0/transformed_0/transformed_.fits.gz out1/distorted_0/distorted_0.fits
# x    y   nx ny zs       infile                      outfile
dislist_file="dislist.txt"  # arg for jedidistort
convlist_file="toconvolvelist.txt"
#-----------------------  source images for jedicatalog  -----------------------
num_source_images=201
# Jedicatalog will read this number of galaxies.
# It also needs to read the four header keys MAG, MAG0, PIXSCALE, and RADIUS.
#
# The code snippets in jedicatalog is: if(strcmp(buffer3,"image")==0 && nimage < num_source_images)
# so it will read these 201 fitsfiles from this config.sh file.
#
# After reading these fitsfiles jedicatalog will create 3 catalog files.
# jedisim_out/out0/trial1_catalog.txt
# jedisim_out/out0/trial1_convolvedlist.txt
# jedisim_out/out0/distortedlist.txt
# Note that jedicatalog do not create any fitsfiles, it will only read
# four header keys from them, and creates three text files.
#-----------------------  source images for jedicatalog  -----------------------
# For adding fake stars to HST.fits
n_stars=200
star_value=100
star_positions="physics_settings/star_positions.txt"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk0.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk1.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk2.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk3.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk4.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk5.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk6.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk7.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk8.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk9.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk10.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk11.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk12.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk13.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk14.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk15.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk16.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk17.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk18.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk19.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk20.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk21.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk22.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk23.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk24.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk25.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk26.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk27.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk28.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk29.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk30.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk31.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk32.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk33.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk34.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk35.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk36.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk37.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk38.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk39.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk40.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk41.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk42.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk43.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk44.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk45.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk46.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk47.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk48.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk49.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk50.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk51.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk52.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk53.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk54.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk55.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk56.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk57.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk58.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk59.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk60.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk61.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk62.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk63.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk64.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk65.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk66.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk67.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk68.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk69.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk70.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk71.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk72.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk73.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk74.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk75.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk76.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk77.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk78.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk79.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk80.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk81.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk82.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk83.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk84.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk85.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk86.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk87.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk88.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk89.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk90.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk91.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk92.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk93.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk94.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk95.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk96.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk97.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk98.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk99.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk100.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk101.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk102.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk103.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk104.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk105.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk106.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk107.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk108.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk109.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk110.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk111.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk112.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk113.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk114.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk115.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk116.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk117.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk118.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk119.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk120.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk121.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk122.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk123.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk124.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk125.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk126.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk127.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk128.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk129.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk130.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk131.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk132.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk133.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk134.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk135.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk136.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk137.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk138.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk139.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk140.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk141.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk142.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk143.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk144.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk145.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk146.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk147.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk148.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk149.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk150.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk151.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk152.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk153.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk154.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk155.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk156.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk157.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk158.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk159.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk160.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk161.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk162.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk163.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk164.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk165.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk166.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk167.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk168.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk169.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk170.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk171.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk172.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk173.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk174.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk175.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk176.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk177.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk178.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk179.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk180.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk181.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk182.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk183.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk184.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk185.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk186.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk187.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk188.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk189.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk190.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk191.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk192.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk193.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk194.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk195.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk196.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk197.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk198.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk199.fits"
image="simdatabase/scaled_disk_f8/f814w_scaled_disk200.fits"
