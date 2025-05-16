#include "database.h"

sqlite3 *db = NULL;
const char *db_name = "passwordManager.db";

int connect_to_database() {
    int rc = sqlite3_open(db_name, &db);
    if (rc) {
        fprintf(stderr, "Can't open database: %s\n", sqlite3_errmsg(db));
        return rc;
    }
    return SQLITE_OK;
}
int checkUser(const char *username, const char *password) {
    sqlite3 *db;
    sqlite3_stmt *stmt;
    int user_exists = 0;
    // Open the database
    int rc = sqlite3_open(db_name, &db);
    if (rc != SQLITE_OK) {
        fprintf(stderr, "Cannot open database: %s\n", sqlite3_errmsg(db));
        return 0;
    }

    const char *sql = "SELECT id FROM users WHERE username = ? AND password = ?;";

    // Prepare the statement FIRST
    rc = sqlite3_prepare_v2(db, sql, -1, &stmt, NULL);
    if (rc != SQLITE_OK) {
        fprintf(stderr, "Failed to prepare statement: %s\n", sqlite3_errmsg(db));
        sqlite3_close(db);
        return 0;
    }


    sqlite3_bind_text(stmt, 1, username, -1, SQLITE_STATIC);
    sqlite3_bind_text(stmt, 2, password, -1, SQLITE_STATIC);

    if (sqlite3_step(stmt) == SQLITE_ROW) user_exists = sqlite3_column_int(stmt, 0);

    sqlite3_finalize(stmt);
    sqlite3_close(db);

    return user_exists;
}

int addUser(const char *username, const char *password){
    sqlite3 *db;
    sqlite3_stmt *stmt;
    int rc = sqlite3_open(db_name, &db);
    if (rc != SQLITE_OK) {
        fprintf(stderr, "Cannot open database: %s\n", sqlite3_errmsg(db));
        return 0;
    }

    const char *sql = "INSERT INTO users (username, password) VALUES (?, ?);";

    rc = sqlite3_prepare_v2(db, sql, -1, &stmt, NULL);
    if (rc != SQLITE_OK) {
        fprintf(stderr, "Failed to prepare statement: %s\n", sqlite3_errmsg(db));
        sqlite3_close(db);
        return 0;
    }

    sqlite3_bind_text(stmt, 1, username, -1, SQLITE_STATIC);
    sqlite3_bind_text(stmt, 2, password, -1, SQLITE_STATIC);

    rc = sqlite3_step(stmt);
    if (rc != SQLITE_DONE) {
        fprintf(stderr, "Execution failed: %s\n", sqlite3_errmsg(db));
        sqlite3_finalize(stmt);
        sqlite3_close(db);
        return 0;
    }

    sqlite3_finalize(stmt);
    sqlite3_close(db);

    return 1;

}

char* checkSite(const char* site, const char* id){
    sqlite3 *db;
    sqlite3_stmt *stmt;
    char* password = NULL;
    int rc = sqlite3_open(db_name, &db);
    if (rc != SQLITE_OK) {
        fprintf(stderr, "Cannot open database: %s\n", sqlite3_errmsg(db));
        return NULL;
    }
    const char *sql = "SELECT password FROM passwords WHERE site = ? AND id = ?;";
    rc = sqlite3_prepare_v2(db, sql, -1, &stmt, NULL); 
    if (rc != SQLITE_OK) {
        fprintf(stderr, "Failed to prepare statement: %s\n", sqlite3_errmsg(db));
        sqlite3_close(db);
        return NULL;
    }
    sqlite3_bind_text(stmt, 1, site, -1, SQLITE_STATIC);
    sqlite3_bind_text(stmt, 2, id, -1, SQLITE_STATIC);
    if (sqlite3_step(stmt) == SQLITE_ROW) {
        const char *pass = (const char *)sqlite3_column_text(stmt, 0);
        password = strdup(pass); // Duplicate the string to return it
    } else {
        fprintf(stderr, "No password found for site: %s\n", site);
    }
    sqlite3_finalize(stmt);
    sqlite3_close(db);
    return password;

}
void free_memory(char* ptr) {
    if(ptr) {
        free(ptr);
        
    }
}

PyObject* createPasswordPy(const char *site, const char *id){
    char *password = CreatePassword();
    if(!password) return NULL;
    sqlite3 *db;
    sqlite3_stmt *stmt;
    int rc = sqlite3_open(db_name, &db);
    if (rc != SQLITE_OK) {
        fprintf(stderr, "Cannot open database: %s\n", sqlite3_errmsg(db));
        return NULL;
    }
    
    const char *sql = "INSERT into passwords values site = ? AND id = ? AND password = ?;";
    rc = sqlite3_prepare_v2(db, sql, -1, &stmt, NULL);
    if (rc != SQLITE_OK) {
        fprintf(stderr, "Failed to prepare statement: %s\n", sqlite3_errmsg(db));
        sqlite3_close(db);
        return NULL;
    }
    sqlite3_bind_text(stmt, 1, site, -1, SQLITE_STATIC);
    sqlite3_bind_text(stmt, 2, id, -1, SQLITE_STATIC);
    sqlite3_bind_text(stmt, 3, password, -1, SQLITE_STATIC);
    rc = sqlite3_step(stmt);
    if (rc != SQLITE_DONE) {
        fprintf(stderr, "Execution failed: %s\n", sqlite3_errmsg(db));
        sqlite3_finalize(stmt);
        sqlite3_close(db);
        free_memory(password);
        return NULL;
    }
    sqlite3_finalize(stmt);
    sqlite3_close(db);

    PyObject *py_result = Py_BuildValue("s", password);
    free_memory(password);
    return py_result;

}



PyObject* wrapping_checkSite(const char *site, const char *id){
    const char *result = checkSite(site, id);
    if(!result){
        return NULL;
    }
    PyObject *py_result = Py_BuildValue("s", result);
    free_memory((char*)result);
    return py_result;



}
