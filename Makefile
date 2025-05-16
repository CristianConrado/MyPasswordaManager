# Toolchain
GO       := go
GCC      := gcc

PY_INC   := /usr/include/python3.10
PY_LIB   := /usr/lib/python3.10/config-3.10-x86_64-linux-gnu

CFLAGS   := -shared -O2 -Wall -Wextra -m64 -fPIC \
            -I$(PY_INC)

LDFLAGS  := -L$(PY_LIB) \
            -lsqlite3 \
            -lpython3.10 \
			./libpasswordcreator.so

# Top‐level
all: libpasswordcreator.so database.so

# 1) Build the Go shared lib
libpasswordcreator.so: PasswordCreator.go
	$(GO) build -buildmode=c-shared -o $@ $<

# 2) Build your C extension, linking to Go, Python, SQLite
database.so: database.c libpasswordcreator.so
	$(GCC) $(CFLAGS) \
	  database.c \
	  -o $@ \
	  $(LDFLAGS)

clean:
	rm -f libpasswordcreator.so libpasswordcreator.h database.so

.PHONY: all clean
