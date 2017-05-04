#include <unistd.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>

int main(int argc, char* argv[]){
  char user[1024];
  int check = getlogin_r(user, sizeof(user));

  printf("The user is: %s\n", user);
  char homedir[1024];
  char *home = "/home/";
  char *adding = "/.vim";

  strcpy(homedir, home);
  strcat(homedir, user);
  strcat(homedir, adding);
  printf("The home dir is: %s\n", homedir);
  return 0;
}
