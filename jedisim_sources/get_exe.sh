for f in *.c;
 do gcc -Wall -O3 -o "${f%.c}" "$f"  -lm -lcfitsio -lfftw3f -lm && mv "${f%.c}" ../executables/;
 chmod a+rwx ../executables/"${f%.c}"
done;