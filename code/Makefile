CFLAGS=
CC=gcc
DEPS = DirOps.h
OBJ = setup.o DirOps.o

%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

setup: $(OBJ) 
	$(CC) -o $@ $^ $(CFLAGS)
	rm *.o

