#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sqlite3.h>


int connect_to_database();
int checkUser(const char *username, const char *password);
int addUser(const char *username, const char *password);