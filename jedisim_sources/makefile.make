CC       =gcc
CFLAGS   =-O3 -Wall
LIB      =-lm -lcfitsio -lfftw3f
EXE_PATH =../executables
SRC_PATH =.

# execute program and clean it
default: jedi
	echo " compilation finished ... "




jedi : jedicatalog jeditransform jedidistort jedipaste jediconvolve jedirescale jedinoise jediaverage

jedicatalog :
	gcc -Wall -O3 $(SRC_PATH)/jedicatalog.c -o $(EXE_PATH)/jedicatalog  $(LIB)

jeditransform :
	$(CC) $(CFLAGS) $(SRC_PATH)/jeditransform.c -o $(EXE_PATH)/jeditransform  $(LIB)

jedidistort :
	$(CC) $(CFLAGS) $(SRC_PATH)/jedidistort.c -o $(EXE_PATH)/jedidistort  $(LIB)

jedipaste :
	$(CC) $(CFLAGS) $(SRC_PATH)/jedipaste.c -o $(EXE_PATH)/jedipaste  $(LIB)

jediconvolve :
	$(CC) $(CFLAGS) $(SRC_PATH)/jediconvolve.c -o $(EXE_PATH)/jediconvolve  $(LIB)

jedirescale :
	$(CC) $(CFLAGS) $(SRC_PATH)/jedirescale.c -o $(EXE_PATH)/jedirescale  $(LIB)

jedinoise :
	$(CC) $(CFLAGS) $(SRC_PATH)/jedinoise.c -o $(EXE_PATH)/jedinoise  $(LIB)

jediaverage :
	$(CC) $(CFLAGS) $(SRC_PATH)/jediaverage.c -o $(EXE_PATH)/jediaverage  $(LIB)

jedicolor :
	$(CC) $(CFLAGS) $(SRC_PATH)/jedicolor.c -o $(EXE_PATH)/jedicolor  $(LIB)


# Utility targets
.PHONY: clean

clean:
	rm -rf $(EXE_PATH)/*.dSYM
