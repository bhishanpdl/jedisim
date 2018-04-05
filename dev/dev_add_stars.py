import numpy as np
from astropy.io import fits
# local imports
from util import replace_outfolder, run_process, updated_config, add_stars, add_wcs

def create_stars_positions(cluster, n_stars,star_value, star_positions):
    # Get values
    n_stars = int(n_stars)
    NAXIS1 = fits.getheader(cluster)['NAXIS1'] # 12288 
    NAXIS2 = fits.getheader(cluster)['NAXIS2'] # 12288 


    # Randomly put stars 
    with open(star_positions,'w') as fo:
      for i in range(0,n_stars):
          x = np.random.randint(0, NAXIS1)
          y = np.random.randint(0, NAXIS2)
          out = '{} {}\n'.format(x,y)
          fo.write(out)
#
def add_stars(cluster, n_stars, star_value,star_positions):
    
    # Make types good
    n_stars = int(n_stars)
    star_value = float(star_value)
  
    # Read cluster
    cluster_hdu = fits.open(cluster,mode='update')
  
    # Randomly put stars inside the cluster
    with open(star_positions,'r') as fi:
        for line in fi.readlines():
            x,y = line.split()
            x,y = int(x), int(y)
            # update the value
            cluster_hdu[0].data[y, x] = star_value
 
    # Write output file
    cluster_hdu.writeto(cluster,clobber=True)
    cluster_hdu.close()          

def main():
    """Run main function."""
    cluster = 'jedisim_out/out0/scaled_bulge/trial1_HST.fits'
    n_stars = 200
    star_value = 100
    star_positions = 'physics_settings/star_positions.txt'
    
    config = updated_config('physics_settings/configb.sh')
    star_positions = config['star_positions']
    print("star_positions = {}".format(star_positions))
    
    # create_stars_positions(cluster, n_stars,star_value, star_positions)
    add_stars(config['HST_image'], config['n_stars'], config['star_value'],config['star_positions'])
    
if __name__ == "__main__":
    main()
