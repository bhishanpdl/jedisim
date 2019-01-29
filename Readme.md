Table of contents
==================
- [Introduction and implementation](#introduction-and-implementation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Outputs](#outputs)
- [Mixed Info](#mixed-info)
- [After the jedisim](#after-the-jedisim)
- [Schematic Diagram](#schematic-diagram)
- [Summary Images](#summary-images)
- [Copyright](#copyright)

![](ohio.png) 

# Introduction and implementation
Jedisim is a program to generate the realistic galaxy cluster simulations from the real
galaxy observation observations.

More information can be found on:
 - jedisim/documentation/jedisim/jedisim.pdf
 - jedisim/documentation/lensing/lensing.pdf
 - jedisim/documentation/Readme.md
    
# Configuration
The settings file for jedisim is `physics_settings/template_config.sh`.
We can change all physics parameter used in jedisim simulation here.
Note that, the extension `.sh` for the config file is just to make the syntax beautiful when we open the file in a text editor, it is not a bash script, which can easily renamed be to `config.txt` or anything else.

# Usage
First we need to create settings files, psfs and scaled galaxies using scripts `a01` to `a07`.
Then we can use the script `jedisim.py` to run other scripts `a08-a11`.
```
python a01_jedisim_config.py -z 1.5  
# physics_settings: configb.sh, configd.sh, configm.sh, lens.txt

python a02_interpolate_sed.py
# sed/exp9_pf_interpolated_z1.5.csv

python a03_scaled_bd_factors.py
# physics_settings/bd_factors.txt

python a04_scaled_gals.py
# simdatabase/scaled_bulge,disk,bulge_disk f8.

python a05_bd_weights_psf.py
# physics_settings/bd_weights_z1.5.txt

python a06_scaled_bd_flux_rat.py
# physics_settings/bd_flux_rat_z1.5.txt

NOTE: Before running a07 script, we need to combine PSF Files
cd psf 
python split_psf_files.py
rm psf*
mv orig_psf/* .
rm -r orig_psf
rm psfb.fits psfd.fits psfm.fits
cd ../
python a07_psf_bdmono.py 
# psf: psfb,psfd,psfm .fits

### Now we can run jedisim.
python jedisim.py
# Runs: a08, a09, a10 and a11 scripts.

python a08_jedisim_odirs.py
# jedisim_out/out0, and out90
## scaled_bulge, scaled_disk scaled_bulge_disk

python a09_jedisim_3cats.py
# jedisim_out/out0,90/trial1_: catalog, convolvedlist, distortgedlist.txt

python a10_jedisimulate.py
# Runs: lsst_TDCR  Transform, Distort, Convolve, Rescale.

python a11_jedisimulate90.py
# Runs: lsst_TDCR  for 90 degree rotated images.
```

To run the simulation multiple time there is a runner script `run_jedisim.py`.
```
python run_jedisim.py -z 0.7 -c pisces -s 0 -e 0
# Here, I am using redshift z as 0.7
# -c is computer name which is running the code
# -s is starting number
# -e is ending number, it is inclusive, -s 0 -e 0 gives only one output.
# run_jedisim.py outputs are written inside **jedisim_outputs**
```

Dependencies:
```
# 1. astropy (pip install astropy )
# 2. util (This is my utility script.)
```

# Outputs

* Output images directory can be changed in the configuration file `physics_settings/template_config.sh`.

* For a single run, the outputs of `jedisim.py` are written inside `jedisim_out/out0` 
  and `jedisim_out/out90` directories.

* For multiple run of the same script `jedisim.py`,  there is a dedicated script `run_jedisim.py`
  which will create outputs inside `jedisim_out/FolderNameWithDate/REDSHIFT/lsst, lsst90, etc`.


# Mixed Info

* The original images of HST ACS WFC are splitted into bulge and disk components using `galfit`.

* The input images for jedisim are `sidmdatabase/bulge_f8` and `sidmdatabase/disk_f8`.
  Here, f8 is the `F814w` filter images I am using for the simulation. We can do it for `F606w`
  and any other bands.
  
* In fact, the correct images that are fed into the end script `jedisim.py` are the 
  `sidmdatabase/scaled_bulge_f8` and `sidmdatabase/scaled_disk_f8` which are created using the 
  script `a04_scaled_gals.py`.

* The radius database for the foreground galaxies are given in `simdatabase/radius_db`.

* The redshift database for the foreground galaxies are given in `simdatabase/red_db`.

* The source codes are in "jedisim_sources/". These are the C programs, 
  which needs to be compiled if we do any changes to these files.

# After the jedisim

* The jedisim outputs, e.g. `jedisim_out/jout_z0.7_2018_04_20_08/z0.7/lsst/lsst_z0.7_0.fits`
  are used in DMStack Mass estimation pipeline to estimate the mass of the 
  background dark matter cluster.
  
# Schematic Diagram
![](images/Jedisim_Diagram.png)

Notes:
> We have 200 galaxies from HST UDF Survey, we create 20,000 images from them using similar radius, magnitude, angle, and so on. Then, we put a lens in between observer and the images background. The lens could be galaxy cluster,  a neutron star, a black hole or any massive object as long as it distorts the background galaxy when an observer observes that galaxy.

> For a single galaxy, we break it into a bulge and a disk using the sodftare **galfit**. Every galaxies have galactic disk, but it may not have bulge. The spiral galaxies generally have both bulge and disk, however, disk galaxies may not have the bulge at the center of the galaxy. In this simulation, if there is no bulge part, we keep it zero pixeled image of the same dimension as that of the disk image.

> After we break a single galaxy to bulge and disk part, we keep the total brightness of bulge+disk same for both HST and LSST, however, the ratio of bulge_to_disk is different for HST and LSST, due to the star formation history in the galaxy.

> When we look at the redshift of galaxies, we take the redshift of the HST galaxies to be $z = 0.2$, and we do our simulation for LSST at user given redshifts (e.g. z = 0.7, 1.0, 1.5 etc).

> In this project we are mainly studying the effect of choice of PSF and its effect on the shear measurement of background galaxies. We study both wavelength dependent (i.e. chromatic) and independent ( i.e. monochromatic) effects.

> The final outputs of jedisim are `lsst.fits` and `lsst_mono.fits`. We also get the 90 degree rotated versions of these outputs
(keeping all other parameters unchanged) so as to reduce the intrinsic shape bias of the background galaxy sample. This means
when we run jedisim, from our initial 200 F814W galaxies, we had created bulge and disk parts of these galaxies, then created 20,000
samples of galaxies using similar parameters and in the end we get only one chromatic galaxy cluster, one monochromatic galaxy cluster and 90-degree rotated versions of them.

> We use the DMStack Pipeline `obs_file` to get the shear estimates of the output galaxies clusters.

> We use the DMStack Pipepline `Clusters` to get the mass estimates of the galaxy clusters.

# Summary Images
![](images/galaxy_fitting.png)
![](images/rescaling_bulge_disk.png)
![](images/psf_from_phosim.png)
![](images/jeditransform.png)
![](images/transform_and_distort.png)
![](images/hst_convolve.png)
![](images/chro_mono.png)

# Copyright
The C-programs and basic skeleton was  was developed by *Daniel Parker*  and *Ian Dell'Antonio* 
of Brown University in around 2013. I forked the project in 2014 and customized the project for the color dependent analysis. I am maintaining this repo from 2014 (though I uploaded it very late) and is being changed constantly.
There is also another repo with more generalized version maintained by [Binyang Liu of Brown University](https://github.com/rbliu/jedisim).<br>
