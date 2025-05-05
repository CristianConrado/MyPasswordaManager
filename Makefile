all:
	gcc -shared -O2 -Wall -Wextra -m64 -fPIC \
  -I/usr/include/python3.10 \
  -L/usr/lib/python3.10/config-3.10-x86_64-linux-gnu \
  database.c -o database.so -lsqlite3 -lpython3.10




clean:
	