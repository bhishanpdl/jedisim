CC=gcc
CFLAGS=-O3 -Wall
LIBS=-I/usr/local/include -I/usr/include -I /Users/poudel/Applications/cfitsio/include  -L /Users/poudel/Applications/cfitsio/lib -lm -lcfitsio


# execute program and clean it
default: jedi
	echo " compilation finished ... "




jedi : jedicatalog jeditransform jedidistort jedipaste jediconvolve jedirescale jedinoise jediaverage jedicolor

jedicatalog :
	gcc -Wall -O3 sources/jedicatalog.c -o executables/jedicatalog $(LIBS) -lm -lcfitsio -lpthread -lfftw3f

jeditransform :
	$(CC) $(CFLAGS) sources/jeditransform.c -o executables/jeditransform $(LIBS)

jedidistort :
	$(CC) $(CFLAGS) sources/jedidistort.c -o executables/jedidistort $(LIBS)

jedipaste :
	$(CC) $(CFLAGS) sources/jedipaste.c -o executables/jedipaste $(LIBS)

jediconvolve :
	$(CC) $(CFLAGS) sources/jediconvolve.c -o executables/jediconvolve $(LIBS) -lfftw3f

jedirescale :
	$(CC) $(CFLAGS) sources/jedirescale.c -o executables/jedirescale $(LIBS)

jedinoise :
	$(CC) $(CFLAGS) sources/jedinoise.c -o executables/jedinoise $(LIBS)

jediaverage :
	$(CC) $(CFLAGS) sources/jediaverage.c -o executables/jediaverage $(LIBS)

jedicolor :
	$(CC) $(CFLAGS) sources/jedicolor.c -o executables/jedicolor $(LIBS)


# Utility targets
.PHONY: clean

clean:
	rm -rf executables/*.dSYM
