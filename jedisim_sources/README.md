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

# Installation of cifitsio and fftw3 in moneta
```bash
# cfitsio
cd ~/Softwares
wget http://www.fftw.org/fftw-3.3.8.tar.gz
gunzip -c fftw-3.3.8.tar.gz
tar -xvf cfitsio-3.47.tar
cd cfitsio-3.47/
./configure --enable--sse2 --enable-reentrant --prefix=/home/poudel/usr/local/
make
make install


# fftw3
cd ~/Softwares
wget http://www.fftw.org/fftw-3.3.8.tar.gz
gunzip -c fftw-3.3.8.tar.gz | tar xv
cd ~/Softwares/fftw-3.3.8/
ls
./configure --enable-float --enable-sse --enable-threads --prefix=/home/poudel/usr/local/
make
make install

# add the paths in ~/.bashrc

##======================================
## dynamic library path for jedisim
##======================================
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/poudel/usr/local/lib64







##======================================
## PATH for cfitsio and fftw3
##======================================
PATH="/home/poudel/usr/local/bin:${PATH}"
export PATH
```

# Install python packages
```bash
# this does not work
#pip install --user --upgrade pip
#pip install --user astropy
#python --version # 2.7.14

pip freeze # shows astropy but python hello.py fails to import astropy
```

# Install miniconda3 in moneta
```bash
cd Softwares/
mkdir myminiconda
cd myminiconda
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh

# hit yes and install miniconda3 with python3.8 in home folder.

After I install miniconda3 these lines will be written at the bottom of ~/.bashrc

# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/home/poudel/miniconda3/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/home/poudel/miniconda3/etc/profile.d/conda.sh" ]; then
        . "/home/poudel/miniconda3/etc/profile.d/conda.sh"
    else
        export PATH="/home/poudel/miniconda3/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<



I also need to add the path of python in bashrc.
##======================================
## Python
##======================================
# Setting PATH for Python 3.8 from miniconda
PATH="/home/poudel/miniconda3/bin:${PATH}"
export PATH

```

# Install python packages
```bash
/home/poudel/miniconda3/bin/pip install astropy scipy pandas
```

# Run jedisim
