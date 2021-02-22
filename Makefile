CC = gcc
CFLAGS = -std=c99

egg: egg.o; $(CC) $(CFLAGS) egg.o -o egg

egg.o: egg.c; $(CC) $(CFLAGS) -c egg.c

clean:; rm -rf *.o ./egg

