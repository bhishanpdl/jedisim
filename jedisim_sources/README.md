# Installing cfitsio
```bash
# download zip file
wget http://heasarc.gsfc.nasa.gov/FTP/software/fitsio/c/cfitsio-3.47.tar.gz

# unzip
gunzip -c cfitsio-3.47.tar.gz | tar xv

# move folder to Softwares
mv cfitsio-3.47 ~/Softwares

# cd to path
cd ~/Softwares/cfitsio-3.47/

# configure
./configure --enable-sse2 --enable-reentrant  --prefix=/usr/local/

# make and install
make
make install
```

# Installing fftw3
```bash
# download zip file
wget http://www.fftw.org/fftw-3.3.8.tar.gz

# unzip
gunzip -c fftw-3.3.8.tar.gz | tar xv

# move folder to Softwares
mv fftw-3.3.8 ~/Softwares

# cd to path
cd ~/Softwares/fftw-3.3.8/

# configure
./configure --enable-float --enable-sse --enable-threads --prefix=/usr/local/

# make and install
make
make install
```

# Compile source codes
```bash
# cd to jedisim sources
# note: we must need last lm command, but first lm is not required.
for f in *.c;
 do gcc -Wall -O3 -o "${f%.c}" "$f"  -lm -lcfitsio -lfftw3f -lm && mv "${f%.c}" ../executables/;
done;
```
