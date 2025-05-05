all:
	gcc -shared -o database.so -m64 -fPIC database.c -lsqlite3