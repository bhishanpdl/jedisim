![](ohio.png) 

# Introduction
Jedisim is a program to generate the realistic galaxy cluster simulations from the real
galaxy observation observations.

> **Copyright**: The original source code was developed by *Daniel Parker* 
  and *Ian Dell'Antonio* of Brown University in around 2013.
  I forked the project in 2014 and customized the jedisim for the color dependent analysis.
  I am maintaining this repo from 2014 (though I uploaded it very late) and is being changed constantly.
  There is also another repo with more generalized version maintained by [Binyang Liu of Brown University](https://github.com/rbliu/jedisim).<br>

-----------

## 1. Introduction and implementation

* Please refer to the documentations:

    * jedisim/documentation/jedisim/jedisim.pdf

    * jedisim/documentation/lensing/lensing.pdf
    
    * jedisim/documentation/Readme.md
    
## 2. Configuration

The settings file for jedisim is `physics_settings/template_config.sh`.
We can change all physics parameter used in jedisim simulation here.

## 3. Usage

The python script to run the jedisim is `jedisim.py`. We can run the jedisim using
folowing command.
```
python jedisim.py
# jedisim.py outputs are inside ***jedisim_out*
```

To run the simulation multiple time there is a runner script `run_jedisim.py`.
```
python run_jedisim.py -z 0.7 -c pisces -s 0 -e 0
# Here, I am using redshift z as 0.7
# -c is computer name which is running the code
# -s is starting number
# -e is ending number, it is inclusive, -s 0 -e 0 gives only one output.
# run_jedisim.py outputs are inside ***jedisim_outputs*
```

Dependencies:
```
# 1. astropy ( to install this run  pip install astropy )
# 2. util   ( This is my local utitily scripts file util.py )
# Note: The code is mainly written in python3, however, it is compatible with python2.
```

## 4. Output

* Specify the directory of output images in configuration file `physics_settings/template_config.sh`.

* For a single run, the outputs of `jedisim.py` are created inside `jedisim_out/out0` 
  and `jedisim_out/out90` directories. Here we have unrotated and 90 degree rotated simulations
  inside out0 and out90, respectively.

* For multiple run of the same script `jedisim.py`,  there is a dedicated script `run_jedisim.py`
  which will create outputs inside `jedisim_out/FolderNameWithDate/REDSHIFT/lsst, lsst90, etc`.


## 5. Others

* The original images of HST ACS WFC are splitted into bulge and disk compontents using `galfit`.

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

## After the jedisim

* The jedisim outputs, e.g. `jedisim_out/jout_z0.7_2018_04_20_08/z0.7/lsst/lsst_z0.7_0.fits`
  are used in DMStack Mass estimation pipeline to estimate the mass of the 
  background dark matter cluster.
