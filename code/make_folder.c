#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <linux/limits.h>
#include <string.h>


int main(int argc, char *argv[]){
  struct stat st = {0};
  char actualpath[PATH_MAX+1];
  char cwd[PATH_MAX+1];
  char *ptr;
  
  char *other;
  char that_one[PATH_MAX+1];

  char test[400];
  int check = getlogin_r(test, sizeof(test));
  printf("user is: %s\n", test);

  if(getcwd(cwd, sizeof(cwd)) != NULL)
  printf("Working directory is: %s\n", cwd);
  ptr = realpath(cwd, actualpath);
  printf("Full directory is: %s\n", ptr);

  strcat(ptr, "/test");
  if(stat(ptr, &st) == -1){
    mkdir(ptr, 0777);
    }
  return 0;
}
