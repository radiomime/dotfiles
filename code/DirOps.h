#ifndef DIROPS_H
#define DIROPS_H


#include <stdio.h>
#include <dirent.h>
#include <stdlib.h>
#include <string.h>

#include <ftw.h>
#include <unistd.h>

int copy(char* from, char* to);
int remove_directory(const char *path);
void ls( char* dir_name, void (*lambda)(char*) );

#endif
